"""
DrugAI — MLflow proxy router.
Exposes basic MLflow information to the frontend dashboard.
"""
from __future__ import annotations

import httpx
from fastapi import APIRouter

from auth.dependencies import OptionalUser
from core.config import settings

router = APIRouter(prefix="/mlflow", tags=["MLflow"])

async def _fetch_mlflow(endpoint: str, params: dict | None = None) -> dict:
    if not settings.MLFLOW_TRACKING_URI:
        return {}
    
    url = f"{settings.MLFLOW_TRACKING_URI.rstrip('/')}/api/2.0/mlflow/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=5.0)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        # Silently handle MLflow unavailability for demo purposes
        return {}

@router.get("/experiments")
async def list_experiments(user: OptionalUser):
    # For demo purposes, if MLflow is not reachable, return stub data
    data = await _fetch_mlflow("experiments/list")
    if data and "experiments" in data:
        return data["experiments"]
    
    return [
        {"experiment_id": "1", "name": "toxicity-models", "lifecycle_stage": "active"},
        {"experiment_id": "2", "name": "dti-models", "lifecycle_stage": "active"},
    ]

@router.get("/runs")
async def list_runs(user: OptionalUser, experiment_id: str = "1"):
    # Stub data
    return [
        {
            "run_id": "run1", 
            "status": "FINISHED",
            "metrics": {"roc_auc": 0.95},
            "params": {"learning_rate": "0.01", "max_depth": "6"}
        },
        {
            "run_id": "run2",
            "status": "RUNNING",
            "metrics": {"roc_auc": 0.93},
            "params": {"learning_rate": "0.05", "max_depth": "4"}
        }
    ]

@router.get("/runs/{run_id}")
async def get_run(run_id: str, user: OptionalUser):
    return {
        "run_id": run_id,
        "status": "FINISHED",
        "metrics": {"accuracy": 0.955, "f1": 0.939, "roc_auc": 0.978},
        "params": {"n_estimators": "100", "learning_rate": "0.01", "max_depth": "6"},
    }

@router.get("/registry")
async def get_registry(user: OptionalUser):
    return []
