"""
DrugAI — Reports router: Generate and download PDF/CSV reports.
"""
from __future__ import annotations

import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy import desc, select

from auth.dependencies import CurrentUser, DBDep
from core.exceptions import NotFoundError
from models.report import Report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/")
async def list_reports(db: DBDep, user: CurrentUser):
    stmt = (
        select(Report)
        .where(Report.user_id == user.id)
        .order_by(desc(Report.created_at))
    )
    result = await db.execute(stmt)
    return [r.to_api_response() for r in result.scalars().all()]

@router.post("/generate")
async def generate_report(
    body: dict,
    db: DBDep,
    user: CurrentUser,
    bg: BackgroundTasks,
):
    report_type = body.get("type", "csv").lower()
    title = body.get("title", f"Report_{uuid.uuid4().hex[:8]}")
    
    # Simple report generation simulation for single compounds (writes a text card)
    report_filename = f"report_{uuid.uuid4().hex[:8]}.{report_type}"
    from core.config import settings
    report_path = settings.reports_path / report_filename
    
    with open(report_path, "w") as f:
        f.write(f"DrugAI Scientific Analysis Report\nTitle: {title}\nGenerated for: {user.email}\n")
        
    report = Report(
        user_id=user.id,
        title=title,
        report_type="research",
        format_=report_type,
        file_path=str(report_path),
        size_bytes=report_path.stat().st_size,
        status="completed",
    )
    db.add(report)
    await db.flush()
    
    return {"message": "Report generation completed.", "reportId": str(report.id)}

@router.get("/{report_id}/download")
async def download_report(report_id: str, db: DBDep, user: CurrentUser):
    try:
        uid = uuid.UUID(report_id)
    except ValueError:
        raise NotFoundError("Invalid report ID.")
        
    result = await db.execute(
        select(Report).where(Report.id == uid, Report.user_id == user.id)
    )
    report = result.scalar_one_or_none()
    if not report or not report.file_path or not os.path.exists(report.file_path):
        raise NotFoundError("Report file not found.")
        
    return FileResponse(
        path=report.file_path,
        filename=os.path.basename(report.file_path),
        media_type="application/octet-stream"
    )
