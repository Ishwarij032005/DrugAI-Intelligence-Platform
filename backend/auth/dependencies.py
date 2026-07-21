"""
DrugAI — FastAPI dependency injection for authentication and RBAC.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.service import get_user_by_id
from core.database import get_db
from core.exceptions import (
    AuthenticationError,
    InsufficientPermissionsError,
    InvalidTokenError,
)
from core.redis_client import is_token_blacklisted
from core.security import decode_token
from models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

DBDep = Annotated[AsyncSession, Depends(get_db)]
BearerDep = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


async def _resolve_user_from_token(
    credentials: BearerDep,
    db: DBDep,
) -> User | None:
    """Extract and validate JWT; return User or None (for optional auth)."""
    if credentials is None:
        return None

    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise InvalidTokenError()

    if payload.get("type") != "access":
        raise InvalidTokenError("Not an access token.")

    # Check blacklist (logout)
    token_id = payload.get("jti")
    if token_id and await is_token_blacklisted(token_id):
        raise InvalidTokenError("Token has been revoked.")

    try:
        user_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError):
        raise InvalidTokenError()

    user = await get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise AuthenticationError("User not found or disabled.")

    return user


async def get_current_user(
    credentials: BearerDep,
    db: DBDep,
) -> User:
    """Strict auth — raises 401 if no valid token."""
    user = await _resolve_user_from_token(credentials, db)
    if user is None:
        raise AuthenticationError("Authentication required.")
    return user


async def get_optional_user(
    credentials: BearerDep,
    db: DBDep,
) -> User | None:
    """Optional auth — returns None if no token (for dev-friendly endpoints)."""
    return await _resolve_user_from_token(credentials, db)


CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalUser = Annotated[User | None, Depends(get_optional_user)]


def require_roles(*roles: str):
    """Factory that creates a dependency requiring one of the specified roles."""
    async def _dep(user: CurrentUser) -> User:
        if user.role not in roles:
            raise InsufficientPermissionsError(
                f"Required role: {' or '.join(roles)}. Your role: {user.role}"
            )
        return user
    return Depends(_dep)


AdminRequired = require_roles("admin")
ResearcherRequired = require_roles("admin", "researcher")
