from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    paper_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)
    return service.get_recommendations(
        paper_id=paper_id,
        limit=limit,
    )