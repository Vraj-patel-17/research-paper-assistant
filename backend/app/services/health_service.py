from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import logging
logger = logging.getLogger(__name__)

class HealthService:
    @staticmethod
    def liveness() -> dict:
        return {
            "status": "alive"
        }

    @staticmethod
    async def readiness(db: AsyncSession) -> dict:
        try:
            await db.execute(text("SELECT 1"))

            return {
                "status": "ready",
                "database": "connected"
            }

        except Exception:
            logger.exception("Database readiness check failed")
            return {
                "status": "not ready",
                "database": "disconnected"
            }