"""
DrugAI — Auth router: all authentication endpoints.
"""
from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import auth.service as svc
from auth.dependencies import CurrentUser, DBDep, get_current_user
from auth.schemas import (
    AccessTokenResponse,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserOut,
    VerifyEmailRequest,
)
from core.logging import get_logger

log = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest, db: DBDep, bg: BackgroundTasks):
    """Create a new account. Returns JWT tokens immediately."""
    user = await svc.register_user(db, body)
    tokens = svc.issue_tokens(user)
    # Send verification email in background (if EMAIL_ENABLED)
    bg.add_task(_maybe_send_verification, user)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DBDep):
    """Authenticate with email + password. Returns access and refresh tokens."""
    user = await svc.authenticate_user(db, body)
    return svc.issue_tokens(user)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(body: RefreshRequest, db: DBDep):
    """Exchange a valid refresh token for a new access token."""
    return await svc.refresh_access_token(db, body.refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout(user: CurrentUser):
    """Invalidate the current session (client should discard tokens)."""
    log.info("user_logout", user_id=str(user.id))
    return {"message": "Logged out successfully."}


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(body: ForgotPasswordRequest, db: DBDep, bg: BackgroundTasks):
    """Send a password reset email (always returns 200 to prevent enumeration)."""
    user = await svc.get_user_by_email(db, body.email)
    if user:
        token = svc.generate_password_reset_token(user)
        bg.add_task(_send_reset_email, user.email, token)
    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(body: ResetPasswordRequest, db: DBDep):
    """Reset password using token from email."""
    await svc.reset_password(db, body.token, body.new_password)
    return {"message": "Password reset successfully. Please log in again."}


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(body: VerifyEmailRequest, db: DBDep):
    """Mark email as verified using token from verification email."""
    await svc.verify_email_token(db, body.token)
    return {"message": "Email verified successfully."}


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(user: CurrentUser, bg: BackgroundTasks):
    """Re-send the email verification link."""
    if user.is_verified:
        return {"message": "Email is already verified."}
    token = svc.generate_email_verification_token(user)
    bg.add_task(_send_verification_email, user.email, token)
    return {"message": "Verification email sent."}


@router.get("/me", response_model=UserOut)
async def get_me(user: CurrentUser):
    """Return the currently authenticated user's profile."""
    return user


@router.patch("/me", response_model=UserOut)
async def update_me(body: UpdateProfileRequest, user: CurrentUser, db: DBDep):
    """Update profile fields and/or change password."""
    updated = await svc.update_user_profile(db, user, body)
    return updated


# ── Background Task Helpers ────────────────────────────────────────────────────

async def _maybe_send_verification(user) -> None:
    from core.config import settings
    if settings.EMAIL_ENABLED and not user.is_verified:
        token = svc.generate_email_verification_token(user)
        await _send_verification_email(user.email, token)


async def _send_verification_email(email: str, token: str) -> None:
    log.info("send_verification_email", email=email, token_preview=token[:20])
    # TODO: integrate email service (tasks/email_tasks.py)


async def _send_reset_email(email: str, token: str) -> None:
    log.info("send_reset_email", email=email, token_preview=token[:20])
    # TODO: integrate email service (tasks/email_tasks.py)
