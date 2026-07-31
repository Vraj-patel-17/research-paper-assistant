from fastapi import APIRouter, Depends ,Path ,Request
from sqlalchemy.orm import Session
from app.core.rate_limiter import limiter
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
@limiter.limit("20/minute")
def chat_with_paper(request:Request,chat_request: ChatRequest,
    paper_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    service = ChatService(db)

    return service.chat(
        paper_id=paper_id,
        question=chat_request.question,
    )