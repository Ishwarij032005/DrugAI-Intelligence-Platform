"""
DrugAI — Seed demo users and initial predictions.
"""
import asyncio

from auth.schemas import RegisterRequest
from auth.service import register_user
from core.config import settings
from core.database import get_db_context
from core.logging import get_logger
from models.prediction import Prediction

log = get_logger(__name__)

async def seed_data():
    async with get_db_context() as db:
        # Create Admin
        try:
            admin_req = RegisterRequest(
                full_name=settings.FIRST_ADMIN_NAME,
                email=settings.FIRST_ADMIN_EMAIL,
                password=settings.FIRST_ADMIN_PASSWORD,
                role="admin",
            )
            admin = await register_user(db, admin_req)
            log.info("admin_created", email=admin.email)
        except Exception as e:
            log.info("admin_exists_or_error", error=str(e))
            
        # Create Researcher
        try:
            res_req = RegisterRequest(
                full_name="Dr. Alex Vance",
                email="researcher@drugai.com",
                password="Researcher@1234",
                role="researcher",
            )
            res = await register_user(db, res_req)
            log.info("researcher_created", email=res.email)
        except Exception as e:
            log.info("researcher_exists_or_error", error=str(e))
            
        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed_data())
