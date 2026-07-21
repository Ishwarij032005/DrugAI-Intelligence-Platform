"""
DrugAI — Seed initial model registry records.
"""
import asyncio

from core.database import get_db_context
from core.logging import get_logger
from models.ml_registry import ModelRegistry
from api.v1.models import _MODEL_CATALOGUE

log = get_logger(__name__)

async def seed_models():
    async with get_db_context() as db:
        for m in _MODEL_CATALOGUE:
            reg = ModelRegistry(
                name=m["name"],
                version=m["version"],
                model_type=m["type"],
                stage=m["stage"],
                metrics={
                    "accuracy": m["accuracy"],
                    "precision": m["precision"],
                    "recall": m["recall"],
                    "f1": m["f1"],
                    "roc_auc": m["roc"],
                    "latency_ms": m["latencyMs"],
                }
            )
            db.add(reg)
        await db.commit()
        log.info("models_seeded", count=len(_MODEL_CATALOGUE))

if __name__ == "__main__":
    asyncio.run(seed_models())
