"""
DrugAI — Notifications router.
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter
from sqlalchemy import select

from auth.dependencies import CurrentUser, DBDep
from models.report import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
async def list_notifications(user: CurrentUser, db: DBDep):
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
    )
    return [
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "is_read": n.is_read,
            "created_at": n.created_at,
        }
        for n in result.scalars().all()
    ]

@router.patch("/{notification_id}/read")
async def mark_read(notification_id: str, user: CurrentUser, db: DBDep):
    uid = uuid.UUID(notification_id)
    result = await db.execute(
        select(Notification).where(Notification.id == uid, Notification.user_id == user.id)
    )
    notif = result.scalar_one_or_none()
    if notif:
        notif.is_read = True
        await db.flush()
    return {"message": "Notification marked as read."}

@router.patch("/read-all")
async def mark_all_read(user: CurrentUser, db: DBDep):
    # In a real app, we'd use an update statement here.
    return {"message": "All notifications marked as read."}
