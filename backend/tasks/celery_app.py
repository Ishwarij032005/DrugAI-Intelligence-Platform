"""
DrugAI — Celery application configuration.
"""
from __future__ import annotations

import os

from celery import Celery

# Use the same Redis URLs as defined in core/config.py
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

celery_app = Celery(
    "drugai_tasks",
    broker=broker_url,
    backend=result_backend,
    include=[
        "tasks.prediction_tasks",
        "tasks.training_tasks",
        "tasks.report_tasks",
        "tasks.email_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600, # 1 hour max for training tasks
)
