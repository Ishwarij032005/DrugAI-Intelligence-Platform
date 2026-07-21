"""
DrugAI — Celery tasks for report generation (PDF/CSV).
"""
from __future__ import annotations

import time
from celery import shared_task

from core.logging import get_logger

log = get_logger(__name__)

@shared_task
def generate_pdf_report(report_id: str, user_id: str, prediction_ids: list[str]):
    """Simulate PDF report generation."""
    log.info("pdf_report_generation_started", report_id=report_id)
    time.sleep(5) # Simulate work
    log.info("pdf_report_generation_completed", report_id=report_id)
    return {"status": "completed", "report_id": report_id, "file_path": f"/reports/{report_id}.pdf"}

@shared_task
def generate_csv_report(report_id: str, user_id: str, query: str):
    """Simulate CSV report generation."""
    log.info("csv_report_generation_started", report_id=report_id)
    time.sleep(3)
    log.info("csv_report_generation_completed", report_id=report_id)
    return {"status": "completed", "report_id": report_id, "file_path": f"/reports/{report_id}.csv"}
