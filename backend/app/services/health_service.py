from sqlalchemy import text
from sqlalchemy.orm import Session
import logging
logger = logging.getLogger(__name__)

class HealthService:
    @staticmethod
    def liveness() -> dict:
        return {
            "status": "alive"
        }

    @staticmethod
    def readiness(db: Session) -> dict:
        try:
            db.execute(text("SELECT 1"))

            return {
                "status": "ready",
                "database": "connected"
            }

        except Exception as exc:
            logger.exception("Database readiness check failed")
            return {
                "status": "not ready",
                "database": "disconnected"
            }