from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
def liveness():
    return HealthService.liveness()


@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    result = await HealthService.readiness(db)

    if result["status"] != "ready":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result,
        )

    return result