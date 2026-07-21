"""
DrugAI — Celery tasks for background and batch predictions.
Supports CSV, SMILES, SDF, and MOL files, parses molecules, runs models, and generates reports.
"""
from __future__ import annotations

import os
import time
import uuid
import asyncio
import pandas as pd
from pathlib import Path
from celery import shared_task
from sqlalchemy import select
from rdkit import Chem

from core.config import settings
from core.database import get_db_context
from core.logging import get_logger
from models.prediction import Prediction
from models.molecule import DrugMolecule
from models.report import Report
from ml.models.base_model import model_manager
from ml.molecular.processor import validate_smiles, compute_properties

log = get_logger(__name__)

@shared_task(bind=True)
def run_batch_prediction(self, file_id: str, user_id: str):
    """
    Background batch prediction task.
    Reads uploaded chemical format files, runs model predictions,
    saves results to database, and generates downloadable CSV report.
    """
    log.info("batch_prediction_started", task_id=self.request.id, file_id=file_id)
    
    # Locate file
    file_path = settings.upload_path / file_id
    if not file_path.exists():
        log.error("batch_file_not_found", path=str(file_path))
        return {"status": "failed", "error": f"File {file_id} not found on disk."}

    # 1. Parse Molecules
    molecules = []
    ext = file_path.suffix.lower()
    
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
            smiles_col = next((c for c in df.columns if c.lower() in ["smiles", "smile", "structure", "compound"]), None)
            name_col = next((c for c in df.columns if c.lower() in ["name", "id", "drug", "drug_id", "title"]), None)
            if not smiles_col:
                raise ValueError("Could not find SMILES column in CSV.")
            for _, row in df.iterrows():
                sm = str(row[smiles_col]).strip()
                nm = str(row[name_col]).strip() if name_col else f"Compound_{len(molecules)+1}"
                if sm and sm != "nan":
                    molecules.append((sm, nm))
                    
        elif ext in [".smi", ".txt"]:
            with open(file_path, "r") as f:
                for idx, line in enumerate(f):
                    parts = line.strip().split()
                    if parts:
                        sm = parts[0]
                        nm = parts[1] if len(parts) > 1 else f"Compound_{idx+1}"
                        molecules.append((sm, nm))
                        
        elif ext == ".sdf":
            suppl = Chem.SDMolSupplier(str(file_path))
            for idx, mol in enumerate(suppl):
                if mol is not None:
                    sm = Chem.MolToSmiles(mol)
                    nm = mol.GetProp("_Name") if mol.HasProp("_Name") else f"SDF_{idx+1}"
                    molecules.append((sm, nm))
                    
        elif ext == ".mol":
            mol = Chem.MolFromMolFile(str(file_path))
            if mol is not None:
                sm = Chem.MolToSmiles(mol)
                nm = mol.GetProp("_Name") if mol.HasProp("_Name") else "MOL_Compound"
                molecules.append((sm, nm))
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    except Exception as e:
        log.error("batch_parsing_failed", error=str(e))
        return {"status": "failed", "error": f"Failed to parse file: {str(e)}"}

    if not molecules:
        return {"status": "failed", "error": "No valid SMILES or molecular structures found in file."}

    total_records = len(molecules)
    processed_count = 0
    results_rows = []

    # Get model predictors
    tox_predictor = model_manager.get("toxicity_ensemble")
    admet_profiler = model_manager.get("admet_profiler")
    dti_predictor = model_manager.get("dti_gcn")
    se_predictor = model_manager.get("side_effects_xgb")

    # Run predictions inside an event loop for database context
    async def process_batch_db():
        nonlocal processed_count
        async with get_db_context() as db:
            for idx, (smiles, name) in enumerate(molecules):
                try:
                    # Validate
                    canonical = validate_smiles(smiles)
                except Exception:
                    # Skip invalid structures
                    continue

                # Predict or load values
                tox_res = tox_predictor.predict(canonical) if tox_predictor else {}
                admet_res = admet_profiler.predict(canonical) if admet_profiler else {}
                dti_res = dti_predictor.predict(canonical) if dti_predictor else {}
                se_res = se_predictor.predict(canonical) if se_predictor else {}

                # Create predictions record
                pred = Prediction(
                    user_id=uuid.UUID(user_id) if user_id else None,
                    input_smiles=smiles,
                    drug_name=name,
                    prediction_type="toxicity",
                    model_used=tox_res.get("modelUsed", "toxicity_ensemble"),
                    result=tox_res,
                    status=tox_res.get("status", "success"),
                    toxicity_score=tox_res.get("toxicity"),
                    confidence_score=tox_res.get("confidence"),
                    processing_time_ms=tox_res.get("processingTimeMs", 0),
                )
                db.add(pred)
                
                # Append to output list
                results_rows.append({
                    "Name": name,
                    "SMILES": smiles,
                    "Toxicity Risk": tox_res.get("riskLevel", "unknown").upper(),
                    "Toxicity Score (%)": tox_res.get("toxicity", 0),
                    "Confidence (%)": tox_res.get("confidence", 0),
                    "Primary Target": dti_res.get("primaryTarget", "N/A"),
                    "Target Affinity (Kd)": dti_res.get("primaryKd", "N/A"),
                })

                processed_count += 1
                
                # Update progress every 10% or at least every 5 molecules
                if idx > 0 and (idx % max(1, total_records // 10) == 0 or idx % 5 == 0):
                    self.update_state(state="PROGRESS", meta={"current": processed_count, "total": total_records})

            # Create Report object
            report_df = pd.DataFrame(results_rows)
            report_filename = f"batch_report_{uuid.uuid4().hex[:8]}.csv"
            report_dest = settings.reports_path / report_filename
            report_df.to_csv(report_dest, index=False)

            report = Report(
                user_id=uuid.UUID(user_id) if user_id else None,
                title=f"Batch Prediction Report ({file_path.name})",
                report_type="batch_csv",
                format_="csv",
                file_path=str(report_dest),
                size_bytes=report_dest.stat().st_size,
                status="completed",
                celery_task_id=self.request.id,
            )
            db.add(report)

    # Run the async loop
    asyncio.run(process_batch_db())

    log.info("batch_prediction_completed", task_id=self.request.id, processed=processed_count)
    return {
        "status": "completed",
        "total_processed": processed_count,
        "total_attempted": total_records,
        "file_id": file_id
    }
