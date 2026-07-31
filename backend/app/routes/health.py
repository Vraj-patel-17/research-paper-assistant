from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
def liveness():
    return HealthService.liveness()


@router.get("/ready")
def readiness(db: Session = Depends(get_db)):
    result = HealthService.readiness(db)

    if result["status"] != "ready":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result,
        )

    return result