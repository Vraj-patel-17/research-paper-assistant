from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.topic import TopicResponse
from app.services.topic_service import TopicService

router = APIRouter(prefix="/topics", tags=["Topics"])
@router.get("", response_model=list[TopicResponse])
async def get_topics(db: AsyncSession = Depends(get_db)):
    service = TopicService(db)
    return await service.list_topics()