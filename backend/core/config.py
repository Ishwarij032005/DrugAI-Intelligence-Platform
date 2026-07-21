"""
DrugAI Platform — Application Configuration
All settings are read from environment variables (with defaults for dev).
"""
from __future__ import annotations

import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────────────────────
    APP_NAME: str = "DrugAI Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_hex(32)
    API_V1_PREFIX: str = "/api/v1"

    # ── CORS ───────────────────────────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: list[str] = [
    # Vite
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # React
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # Backend
    "http://localhost:8000",
    "http://127.0.0.1:8000",

    # Local network (your current frontend)
    "http://10.230.200.45:8080",
    "http://10.230.200.45:5173",
]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except Exception:
                return [i.strip() for i in v.split(",")]
        return v

    # ── Database ───────────────────────────────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/drugai"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/drugai"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # ── Redis ──────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── JWT ────────────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = secrets.token_hex(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── MLflow ─────────────────────────────────────────────────────────────────
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "drugai-experiments"
    MLFLOW_ARTIFACT_ROOT: str = "./mlflow-artifacts"

    # ── File Storage ───────────────────────────────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    REPORTS_DIR: str = "./reports"
    MODELS_DIR: str = "./ml_models"
    DATASETS_DIR: str = "../DrugAI_Synthetic_Dataset_Bundle"
    MAX_UPLOAD_SIZE_MB: int = 100

    # ── Email ──────────────────────────────────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "noreply@drugai.com"
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_NAME: str = "DrugAI Platform"
    EMAILS_FROM_EMAIL: str = "noreply@drugai.com"
    EMAIL_ENABLED: bool = False

    # ── Rate Limiting ──────────────────────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10

    # ── Admin Seed ─────────────────────────────────────────────────────────────
    FIRST_ADMIN_EMAIL: str = "admin@drugai.com"
    FIRST_ADMIN_PASSWORD: str = "Admin@1234"
    FIRST_ADMIN_NAME: str = "Dr. Emily Sinclair"

    # ── Derived Properties ─────────────────────────────────────────────────────
    @property
    def upload_path(self) -> Path:
        p = Path(self.UPLOAD_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def reports_path(self) -> Path:
        p = Path(self.REPORTS_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def models_path(self) -> Path:
        p = Path(self.MODELS_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def datasets_path(self) -> Path:
        return Path(self.DATASETS_DIR)

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
