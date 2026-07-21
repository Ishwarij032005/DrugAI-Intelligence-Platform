"""
DrugAI Intelligence Platform — FastAPI Application Entry Point.
"""
from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from core.config import settings
from core.database import create_tables, dispose_engine
from core.exceptions import register_exception_handlers
from core.logging import configure_logging, get_logger, new_request_id
from core.redis_client import close_redis, get_redis

log = get_logger(__name__)

# ── Rate Limiter ───────────────────────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


# ── Lifespan ───────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(debug=settings.DEBUG)
    log.info("DrugAI starting up", env=settings.ENVIRONMENT)

    # Ensure upload/report directories exist
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    settings.reports_path.mkdir(parents=True, exist_ok=True)
    settings.models_path.mkdir(parents=True, exist_ok=True)

    # Test Redis
    try:
        redis = get_redis()
        await redis.ping()
        log.info("Redis connected")
    except Exception as e:
        log.warning("Redis unavailable", error=str(e))

    # Create tables in dev (Alembic handles prod)
    if settings.is_development:
        try:
            await create_tables()
            log.info("Database tables verified")
        except Exception as e:
            log.warning("Could not create tables", error=str(e))

    # Register and load all ML models
    try:
        import ml.models.toxicity.model  # noqa: F401
        import ml.models.admet.model     # noqa: F401
        import ml.models.dti.model       # noqa: F401
        import ml.models.side_effects.model  # noqa: F401
        import ml.models.similarity.model    # noqa: F401
        log.info("ML models registered")
    except Exception as e:
        log.warning("ML model registration failed", error=str(e))

    yield

    log.info("DrugAI shutting down")
    await dispose_engine()
    await close_redis()


# ── App Factory ────────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Production-grade AI Drug Discovery Platform. "
            "Toxicity prediction, ADMET profiling, DTI, and explainable AI."
        ),
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ── Middleware ─────────────────────────────────────────────────────────────
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Request ID + timing middleware
    @app.middleware("http")
    async def request_middleware(request: Request, call_next) -> Response:
        rid = new_request_id()
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = rid
        response.headers["X-Process-Time"] = f"{elapsed_ms:.2f}ms"
        log.info(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(elapsed_ms, 2),
        )
        return response

    # ── Exception Handlers ─────────────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ───────────────────────────────────────────────────────────────
    from api.v1.router import api_router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # ── Health Endpoints ──────────────────────────────────────────────────────
    @app.get("/health", tags=["Health"])
    async def health():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "DrugAI Intelligence Platform API",
            "docs": "/docs",
            "version": settings.APP_VERSION,
        }

    return app


app = create_app()
