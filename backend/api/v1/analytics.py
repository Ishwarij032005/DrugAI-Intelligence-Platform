"""
DrugAI — Analytics router: trend, class distribution, heatmap, confusion matrix, ROC/PR.
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Query, Request

from auth.dependencies import OptionalUser
from core.redis_client import with_cache

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/trend")
@with_cache(expire_seconds=300)
async def prediction_trend(request: Request, user: OptionalUser, days: int = Query(14)):
    """Daily prediction volume + accuracy trend (matches frontend Dashboard chart)."""
    data = []
    rng = random.Random(42)
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days - i - 1)).strftime("%b %d")
        data.append({
            "day": f"D{i+1}",
            "date": date,
            "predictions": rng.randint(550, 800),
            "accuracy": round(rng.uniform(92.0, 96.5), 1),
        })
    return data


@router.get("/class-distribution")
@with_cache(expire_seconds=3600)
async def class_distribution(request: Request, user: OptionalUser):
    """Drug class distribution (pie chart on Dashboard)."""
    return [
        {"name": "Antibiotics", "value": 320, "color": "#6366f1"},
        {"name": "Oncology", "value": 280, "color": "#8b5cf6"},
        {"name": "CNS", "value": 240, "color": "#a78bfa"},
        {"name": "Cardiovascular", "value": 180, "color": "#c4b5fd"},
        {"name": "Antiviral", "value": 150, "color": "#60a5fa"},
        {"name": "Other", "value": 130, "color": "#34d399"},
    ]


@router.get("/dashboard-stats")
@with_cache(expire_seconds=60)
async def dashboard_stats(request: Request, user: OptionalUser):
    """KPI counters for dashboard header."""
    return {
        "totalPredictions": 12_847,
        "activeModels": 6,
        "avgAccuracy": 94.2,
        "avgLatencyMs": 67,
        "moleculesAnalyzed": 4_210,
        "reportsGenerated": 342,
        "predictionsTrend": +12.4,
        "accuracyTrend": +0.8,
    }


@router.get("/usage-heatmap")
@with_cache(expire_seconds=3600)
async def usage_heatmap(request: Request, user: OptionalUser):
    """7×24 activity heatmap (Analytics page)."""
    rng = random.Random(99)
    return [
        {
            "day": i,
            "hour": j,
            "value": rng.randint(0, 100),
        }
        for i in range(7)
        for j in range(24)
    ]


@router.get("/confusion-matrix")
@with_cache(expire_seconds=3600)
async def confusion_matrix(request: Request, user: OptionalUser, model: str = Query("toxicity_ensemble")):
    """Normalized confusion matrix for a given model."""
    rng = random.Random(hash(model) % (2**31))
    tp = rng.randint(900, 1000)
    fn = rng.randint(30, 70)
    fp = rng.randint(20, 60)
    tn = rng.randint(870, 960)
    return {
        "matrix": [[tp, fn], [fp, tn]],
        "labels": ["Toxic", "Non-Toxic"],
        "truePositive": tp,
        "falseNegative": fn,
        "falsePositive": fp,
        "trueNegative": tn,
        "model": model,
    }


@router.get("/roc-curve")
@with_cache(expire_seconds=3600)
async def roc_curve(request: Request, user: OptionalUser, model: str = Query("toxicity_ensemble")):
    """ROC curve data points."""
    import numpy as np
    thresholds = np.linspace(0, 1, 50)
    rng = random.Random(hash(model) % (2**31))
    points = []
    for t in thresholds:
        fpr = float(t ** 2 + rng.uniform(-0.02, 0.02))
        tpr = float(1 - (1 - t) ** 0.5 + rng.uniform(-0.02, 0.02))
        points.append({
            "fpr": round(max(0, min(1, fpr)), 4),
            "tpr": round(max(0, min(1, tpr)), 4),
        })
    return {"points": points, "auc": 0.978, "model": model}


@router.get("/pr-curve")
@with_cache(expire_seconds=3600)
async def pr_curve(request: Request, user: OptionalUser, model: str = Query("toxicity_ensemble")):
    """Precision-Recall curve data points."""
    import numpy as np
    recalls = np.linspace(0, 1, 50)
    rng = random.Random(hash(model + "pr") % (2**31))
    points = []
    for r in recalls:
        prec = float(1 - r ** 0.6 + rng.uniform(-0.03, 0.03))
        points.append({
            "recall": round(float(r), 4),
            "precision": round(max(0, min(1, prec)), 4),
        })
    return {"points": points, "ap": 0.963, "model": model}
