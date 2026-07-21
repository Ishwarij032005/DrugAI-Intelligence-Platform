"""
DrugAI — Predictions router: all AI prediction endpoints.
"""
from __future__ import annotations

import time
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import DBDep, OptionalUser
from core.exceptions import InvalidSMILESError, PredictionError
from core.logging import get_logger
from ml.models.base_model import model_manager
from ml.molecular.processor import validate_smiles
from models.prediction import Prediction

log = get_logger(__name__)
router = APIRouter(prefix="/predictions", tags=["Predictions"])


def _get_or_demo_user_id(user) -> str:
    """Return user ID string or 'demo' for unauthenticated requests."""
    return str(user.id) if user else "demo"


# ── List Predictions ───────────────────────────────────────────────────────────

@router.get("/")
async def list_predictions(
    db: DBDep,
    user: OptionalUser,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query("", alias="search"),
    prediction_type: str = Query("", alias="type"),
    status: str = Query("", alias="status"),
):
    stmt = (
        select(Prediction)
        .where(Prediction.deleted_at.is_(None))
        .order_by(desc(Prediction.created_at))
    )
    if user:
        stmt = stmt.where(Prediction.user_id == user.id)
    if search:
        stmt = stmt.where(
            Prediction.drug_name.ilike(f"%{search}%")
            | Prediction.input_smiles.ilike(f"%{search}%")
        )
    if prediction_type:
        stmt = stmt.where(Prediction.prediction_type == prediction_type)
    if status:
        stmt = stmt.where(Prediction.status == status)

    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)

    result = await db.execute(stmt)
    preds = result.scalars().all()

    return [p.to_list_item() for p in preds]


# ── Toxicity Prediction ────────────────────────────────────────────────────────

@router.post("/toxicity")
async def predict_toxicity(
    body: dict,
    db: DBDep,
    user: OptionalUser,
):
    smiles = body.get("smiles", "").strip()
    if not smiles:
        raise InvalidSMILESError("SMILES is required.")

    try:
        canonical = validate_smiles(smiles)
    except InvalidSMILESError:
        raise

    predictor = model_manager.get("toxicity_ensemble")
    if predictor is None:
        # Model not yet registered — import triggers self-registration
        try:
            import ml.models.toxicity.model  # noqa: F401
            predictor = model_manager.get("toxicity_ensemble")
        except Exception:
            pass
    if predictor is None:
        raise PredictionError("Toxicity model not available.")

    start = time.perf_counter()
    result = predictor.predict(canonical)
    elapsed = int((time.perf_counter() - start) * 1000)

    # Persist to DB
    pred = Prediction(
        user_id=user.id if user else None,
        input_smiles=smiles,
        drug_name=body.get("name"),
        prediction_type="toxicity",
        model_used=result.get("modelUsed", "toxicity_ensemble"),
        result=result,
        status=result.get("status", "success"),
        toxicity_score=result.get("toxicity"),
        confidence_score=result.get("confidence"),
        processing_time_ms=elapsed,
    )
    db.add(pred)
    await db.flush()

    return {**result, "predictionId": str(pred.id)}


# ── ADMET ──────────────────────────────────────────────────────────────────────

@router.get("/admet")
@router.post("/admet")
async def admet_profile(
    db: DBDep,
    user: OptionalUser,
    body: dict | None = None,
    smiles: str = Query("CC(=O)OC1=CC=CC=C1C(=O)O", alias="smiles"),
):
    target_smiles = (body or {}).get("smiles", smiles)
    try:
        canonical = validate_smiles(target_smiles)
    except Exception:
        canonical = target_smiles

    predictor = model_manager.get("admet_profiler")
    result = predictor.predict(canonical) if predictor else {"admet": []}
    return result["admet"]


# ── DTI ───────────────────────────────────────────────────────────────────────

@router.post("/dti")
async def predict_dti(
    body: dict,
    db: DBDep,
    user: OptionalUser,
):
    smiles = body.get("drug", body.get("smiles", "CC(=O)OC1=CC=CC=C1C(=O)O"))
    protein = body.get("protein", "BCR-ABL1")

    predictor = model_manager.get("dti_gcn")
    result = predictor.predict(smiles, protein=protein) if predictor else {}

    pred = Prediction(
        user_id=user.id if user else None,
        input_smiles=smiles,
        prediction_type="dti",
        model_used="dti_gcn",
        result=result,
        status="success",
    )
    db.add(pred)
    await db.flush()

    return {**result, "predictionId": str(pred.id)}


# ── Side Effects ───────────────────────────────────────────────────────────────

@router.get("/side-effects")
@router.post("/side-effects")
async def predict_side_effects(
    db: DBDep,
    user: OptionalUser,
    body: dict | None = None,
    smiles: str = Query("CC(=O)OC1=CC=CC=C1C(=O)O", alias="smiles"),
):
    target = (body or {}).get("smiles", smiles)
    predictor = model_manager.get("side_effects_xgb")
    result = predictor.predict(target) if predictor else {"sideEffects": []}
    return result["sideEffects"]


# ── Recommendations ────────────────────────────────────────────────────────────

@router.get("/recommendations")
@router.post("/recommendations")
async def drug_recommendations(
    db: DBDep,
    user: OptionalUser,
    body: dict | None = None,
    smiles: str = Query("CC(=O)OC1=CC=CC=C1C(=O)O", alias="smiles"),
    top_k: int = Query(4, alias="topK"),
):
    target = (body or {}).get("smiles", smiles)
    predictor = model_manager.get("recommendation_engine")
    result = predictor.predict(target, top_k=top_k) if predictor else {"recommendations": []}
    return result["recommendations"]


# ── Get Single Prediction ──────────────────────────────────────────────────────

@router.get("/{prediction_id}")
async def get_prediction(prediction_id: str, db: DBDep, user: OptionalUser):
    from core.exceptions import NotFoundError
    try:
        uid = uuid.UUID(prediction_id)
    except ValueError:
        raise NotFoundError("Invalid prediction ID format.")

    result = await db.execute(
        select(Prediction).where(
            Prediction.id == uid, Prediction.deleted_at.is_(None)
        )
    )
    pred = result.scalar_one_or_none()
    if not pred:
        raise NotFoundError("Prediction not found.")
    return {**pred.result, "predictionId": str(pred.id), **pred.to_list_item()}


# ── Explain Prediction ─────────────────────────────────────────────────────────

@router.get("/{prediction_id}/explain")
async def explain_prediction(prediction_id: str, db: DBDep, user: OptionalUser):
    from core.exceptions import NotFoundError
    from ml.explainability.explainer import compute_shap_explanation, compute_lime_explanation

    try:
        uid = uuid.UUID(prediction_id)
    except ValueError:
        raise NotFoundError("Invalid prediction ID.")

    result = await db.execute(
        select(Prediction).where(Prediction.id == uid)
    )
    pred = result.scalar_one_or_none()
    if not pred:
        raise NotFoundError("Prediction not found.")

    shap = compute_shap_explanation(pred.input_smiles, pred.result, pred.model_used)
    lime = compute_lime_explanation(pred.input_smiles, pred.result)

    return {"shap": shap, "lime": lime, "predictionId": prediction_id}


# ── Delete Prediction ──────────────────────────────────────────────────────────

@router.delete("/{prediction_id}")
async def delete_prediction(prediction_id: str, db: DBDep, user: OptionalUser):
    from core.exceptions import NotFoundError
    from datetime import datetime, timezone

    try:
        uid = uuid.UUID(prediction_id)
    except ValueError:
        raise NotFoundError("Invalid prediction ID.")

    result = await db.execute(
        select(Prediction).where(Prediction.id == uid)
    )
    pred = result.scalar_one_or_none()
    if not pred:
        raise NotFoundError("Prediction not found.")

    pred.deleted_at = datetime.now(timezone.utc)
    return {"message": "Prediction deleted."}


# ── Batch Prediction ──────────────────────────────────────────────────────────

@router.post("/batch")
async def batch_predict(body: dict, db: DBDep, user: OptionalUser):
    file_id = body.get("fileId")
    from tasks.prediction_tasks import run_batch_prediction
    task = run_batch_prediction.delay(file_id, _get_or_demo_user_id(user))
    return {"jobId": task.id, "status": "queued", "message": "Batch prediction queued."}
