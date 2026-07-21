"""
DrugAI — Custom exception hierarchy and global exception handlers.
"""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# ── Base ───────────────────────────────────────────────────────────────────────

class DrugAIException(Exception):
    """Base exception for all DrugAI errors."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred."
    headers: dict[str, str] | None = None

    def __init__(
        self,
        detail: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.detail = detail or self.__class__.detail
        self.headers = headers or self.__class__.headers
        super().__init__(self.detail)


# ── Auth Exceptions ────────────────────────────────────────────────────────────

class AuthenticationError(DrugAIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication required."
    headers = {"WWW-Authenticate": "Bearer"}


class InvalidTokenError(AuthenticationError):
    detail = "Invalid or expired token."


class InsufficientPermissionsError(DrugAIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to perform this action."


class AccountDisabledError(AuthenticationError):
    detail = "Your account has been disabled. Contact support."


class EmailNotVerifiedError(AuthenticationError):
    detail = "Please verify your email address before logging in."


# ── Resource Exceptions ────────────────────────────────────────────────────────

class NotFoundError(DrugAIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found."


class ConflictError(DrugAIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists."


class ValidationError(DrugAIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Validation failed."


# ── Molecular Exceptions ───────────────────────────────────────────────────────

class InvalidSMILESError(DrugAIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid SMILES string. Could not parse molecular structure."


class MoleculeProcessingError(DrugAIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Failed to process molecule."


# ── ML Exceptions ─────────────────────────────────────────────────────────────

class ModelNotFoundError(NotFoundError):
    detail = "ML model not found or not loaded."


class PredictionError(DrugAIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Prediction failed. Please try again."


class TrainingError(DrugAIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Model training failed."


# ── Rate Limiting ──────────────────────────────────────────────────────────────

class RateLimitError(DrugAIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Too many requests. Please slow down."


# ── Handlers ───────────────────────────────────────────────────────────────────

def _error_response(
    status_code: int,
    detail: str,
    headers: dict[str, str] | None = None,
    extra: dict[str, Any] | None = None,
) -> JSONResponse:
    content: dict[str, Any] = {"detail": detail, "status_code": status_code}
    if extra:
        content.update(extra)
    return JSONResponse(status_code=status_code, content=content, headers=headers)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DrugAIException)
    async def drugai_exception_handler(
        request: Request, exc: DrugAIException
    ) -> JSONResponse:
        return _error_response(exc.status_code, exc.detail, exc.headers)

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Any) -> JSONResponse:
        return _error_response(404, "The requested endpoint does not exist.")

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Any) -> JSONResponse:
        return _error_response(500, "Internal server error. Please try again.")
