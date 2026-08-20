from fastapi import APIRouter, Depends,  Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.schemas.paper import PaperDetailResponse
from app.services.recommendation_service import RecommendationService
router = APIRouter(
    prefix="/papers",
    tags=["Recommendations"],
)
@router.get(
    "/{paper_id}/recommendations",
    response_model=list[PaperDetailResponse],
)
def get_recommendations(
    paper_id:UUID ,
    limit: int = Query(default=10, ge=1, le=20),
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)
    return service.get_recommendations(
        paper_id=paper_id,
        limit=limit,
    )