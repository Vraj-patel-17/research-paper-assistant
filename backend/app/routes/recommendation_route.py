from fastapi import APIRouter, Depends,  Query
from sqlalchemy.ext.asyncio import AsyncSession
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
async def get_recommendations(
    paper_id:UUID ,
    limit: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    service = RecommendationService(db)
    return await service.get_recommendations(
        paper_id=paper_id,
        limit=limit,
    )