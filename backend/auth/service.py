"""
DrugAI — Auth service: register, login, token management, email verification.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import RegisterRequest, LoginRequest, UpdateProfileRequest
from core.exceptions import (
    AuthenticationError,
    ConflictError,
    InvalidTokenError,
    NotFoundError,
    ValidationError,
)
from core.logging import get_logger
from core.security import (
    create_access_token,
    create_refresh_token,
    create_url_safe_token,
    decode_token,
    decode_url_safe_token,
    hash_password,
    verify_password,
)
from models.user import User, Organization

log = get_logger(__name__)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email.lower(), User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id, User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def register_user(db: AsyncSession, data: RegisterRequest) -> User:
    email = data.email.lower()

    # Check for existing
    existing = await get_user_by_email(db, email)
    if existing:
        raise ConflictError("An account with this email already exists.")

    # Create default organization for user
    org = Organization(
        name=f"{data.full_name}'s Lab",
        slug=f"org-{str(uuid.uuid4())[:8]}",
        plan="research",
    )
    db.add(org)
    await db.flush()

    user = User(
        email=email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=data.role,
        org_id=org.id,
        is_active=True,
        is_verified=True,  # Auto-verify in dev; set False + send email in prod
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    log.info("user_registered", email=email, role=data.role)
    return user


async def authenticate_user(db: AsyncSession, data: LoginRequest) -> User:
    user = await get_user_by_email(db, data.email.lower())
    if not user or not verify_password(data.password, user.hashed_password):
        raise AuthenticationError("Invalid email or password.")

    if not user.is_active:
        raise AuthenticationError("Your account has been disabled. Contact support.")

    # Update last_login
    user.last_login_at = datetime.now(timezone.utc)
    await db.flush()

    return user


def issue_tokens(user: User) -> dict:
    access = create_access_token(str(user.id), role=user.role)
    refresh = create_refresh_token(str(user.id))
    from core.config import settings
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise InvalidTokenError("Token is not a refresh token.")
        user_id = uuid.UUID(payload["sub"])
    except Exception:
        raise InvalidTokenError("Invalid or expired refresh token.")

    user = await get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise AuthenticationError("User not found or disabled.")

    from core.config import settings
    access = create_access_token(str(user.id), role=user.role)
    return {
        "access_token": access,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


async def update_user_profile(
    db: AsyncSession, user: User, data: UpdateProfileRequest
) -> User:
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.job_title is not None:
        user.job_title = data.job_title
    if data.institution is not None:
        user.institution = data.institution
    if data.new_password:
        if not data.current_password or not verify_password(
            data.current_password, user.hashed_password
        ):
            raise ValidationError("Current password is incorrect.")
        user.hashed_password = hash_password(data.new_password)
    await db.flush()
    await db.refresh(user)
    return user


def generate_password_reset_token(user: User) -> str:
    return create_url_safe_token({"sub": str(user.id), "type": "reset"}, expire_hours=2)


async def reset_password(db: AsyncSession, token: str, new_password: str) -> None:
    try:
        payload = decode_url_safe_token(token)
        if payload.get("type") != "reset":
            raise InvalidTokenError()
        user_id = uuid.UUID(payload["sub"])
    except Exception:
        raise InvalidTokenError("Invalid or expired password reset token.")

    user = await get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found.")
    user.hashed_password = hash_password(new_password)
    await db.flush()
    log.info("password_reset", user_id=str(user_id))


def generate_email_verification_token(user: User) -> str:
    return create_url_safe_token({"sub": str(user.id), "type": "verify"}, expire_hours=48)


async def verify_email_token(db: AsyncSession, token: str) -> User:
    try:
        payload = decode_url_safe_token(token)
        if payload.get("type") != "verify":
            raise InvalidTokenError()
        user_id = uuid.UUID(payload["sub"])
    except Exception:
        raise InvalidTokenError("Invalid or expired verification token.")

    user = await get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found.")
    user.is_verified = True
    await db.flush()
    return user
