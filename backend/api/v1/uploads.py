"""
DrugAI — Uploads router for molecules, CSVs, and SDFs.
"""
from __future__ import annotations

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File

from auth.dependencies import OptionalUser
from core.config import settings
from core.logging import get_logger

router = APIRouter(prefix="/upload", tags=["Uploads"])
log = get_logger(__name__)

@router.post("/molecule")
async def upload_molecule(user: OptionalUser, file: UploadFile = File(...)):
    # Read file content and try to parse it as SMILES/MOL
    content = await file.read()
    text = content.decode("utf-8", errors="ignore").strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Simple parsing of single smiles from file
    smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
    if lines:
        first_line = lines[0].split()[0] # get first column
        if len(first_line) > 2:
            smiles = first_line
            
    return {"smiles": smiles, "name": file.filename}

@router.post("/batch-csv")
async def upload_batch_csv(user: OptionalUser, file: UploadFile = File(...)):
    file_id = f"csv-{uuid.uuid4()}"
    ext = Path(file.filename).suffix or ".csv"
    dest_path = settings.upload_path / f"{file_id}{ext}"
    
    # Save file to disk
    content = await file.read()
    with open(dest_path, "wb") as f:
        f.write(content)
        
    log.info("batch_csv_uploaded", filename=file.filename, saved_to=str(dest_path))
    return {"fileId": f"{file_id}{ext}", "message": "Batch CSV file uploaded successfully."}

@router.post("/sdf")
async def upload_sdf(user: OptionalUser, file: UploadFile = File(...)):
    file_id = f"sdf-{uuid.uuid4()}"
    ext = Path(file.filename).suffix or ".sdf"
    dest_path = settings.upload_path / f"{file_id}{ext}"
    
    content = await file.read()
    with open(dest_path, "wb") as f:
        f.write(content)
        
    log.info("sdf_uploaded", filename=file.filename, saved_to=str(dest_path))
    return {"fileId": f"{file_id}{ext}", "message": "SDF file uploaded successfully."}
