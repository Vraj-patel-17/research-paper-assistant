from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.topic import TopicResponse
from app.services.topic_service import TopicService

router = APIRouter(prefix="/topics", tags=["Topics"])
@router.get("", response_model=list[TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    service = TopicService(db)
    return service.list_topics()