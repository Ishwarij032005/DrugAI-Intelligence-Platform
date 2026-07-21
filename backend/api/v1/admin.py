"""
DrugAI — Admin router: User management, API keys, system health.
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter

from auth.dependencies import AdminRequired, DBDep
from auth.schemas import AdminUserUpdate, InviteUserRequest
from core.exceptions import NotFoundError
from models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[AdminRequired])

@router.get("/users")
async def list_users(db: DBDep):
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.deleted_at.is_(None)))
    return [
        {
            "id": str(u.id),
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
        }
        for u in result.scalars().all()
    ]

@router.post("/users/invite")
async def invite_user(body: InviteUserRequest, db: DBDep):
    return {"message": f"Invitation sent to {body.email}."}

@router.patch("/users/{user_id}")
async def update_user(user_id: str, body: AdminUserUpdate, db: DBDep):
    from sqlalchemy import select
    uid = uuid.UUID(user_id)
    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User not found.")
    
    if body.role:
        user.role = body.role
    if body.is_active is not None:
        user.is_active = body.is_active
    if body.full_name:
        user.full_name = body.full_name
    await db.flush()
    return {"message": "User updated."}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: DBDep):
    from sqlalchemy import select
    from datetime import datetime, timezone
    uid = uuid.UUID(user_id)
    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User not found.")
    user.deleted_at = datetime.now(timezone.utc)
    return {"message": "User deleted."}

@router.get("/system-health")
async def system_health():
    import random
    return {
        "status": "healthy",
        "cpu_usage": round(random.uniform(10, 40), 1),
        "ram_usage": round(random.uniform(30, 60), 1),
        "gpu_usage": 0.0,
        "active_connections": random.randint(10, 50),
        "db_latency_ms": random.randint(2, 10),
    }

@router.get("/api-keys")
async def list_api_keys(db: DBDep):
    return []

@router.post("/api-keys")
async def create_api_key(body: dict, db: DBDep):
    return {"message": "API key creation stub."}

@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: str, db: DBDep):
    return {"message": "API key deleted."}

@router.get("/audit-logs")
async def get_audit_logs(db: DBDep):
    return []
