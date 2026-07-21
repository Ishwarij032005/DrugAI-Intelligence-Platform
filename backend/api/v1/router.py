"""
DrugAI — Main API v1 router: assembles all sub-routers.
"""
from fastapi import APIRouter

from auth.router import router as auth_router
from api.v1.predictions import router as predictions_router
from api.v1.molecules import router as molecules_router
from api.v1.models import router as models_router
from api.v1.analytics import router as analytics_router
from api.v1.mlflow_proxy import router as mlflow_router
from api.v1.reports import router as reports_router
from api.v1.admin import router as admin_router
from api.v1.uploads import router as uploads_router
from api.v1.notifications import router as notifications_router
from api.v1.websocket import router as ws_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(predictions_router)
api_router.include_router(molecules_router)
api_router.include_router(models_router)
api_router.include_router(analytics_router)
api_router.include_router(mlflow_router)
api_router.include_router(reports_router)
api_router.include_router(admin_router)
api_router.include_router(uploads_router)
api_router.include_router(notifications_router)
api_router.include_router(ws_router)
