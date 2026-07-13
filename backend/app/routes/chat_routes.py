from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
router = APIRouter(
    prefix="/papers",
    tags=["Paper Chat"],
)
@router.post(
    "/{paper_id}/chat",
    response_model=ChatResponse,
)
def chat_with_paper(
    paper_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    service = ChatService(db)

    return service.chat(
        paper_id=paper_id,
        question=request.question,
    )