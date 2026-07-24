from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional
from app.services.paper_services import get_all_papers,get_paper_by_id
from app.schemas.paper import PaperDetailResponse
from fastapi import Depends,HTTPException
from app.schemas.retrieval import RetrievalDebugResponse
from app.services.chat_service import ChatService
router=APIRouter()
@router.get("/papers")
def get_papers(db:Session=Depends(get_db),q: Optional[str] = None,source: Optional[str] = None,topic:Optional[str]=None,limit: int = 20,offset: int = 0,):
    return get_all_papers(
        db=db,
        q=q,
        source=source,
        topic=topic,
        limit=limit,
        offset=offset,
    )

@router.get("/papers/{paper_id}",response_model=PaperDetailResponse)
def get_paper_from_id(paper_id:int,db:Session=Depends(get_db)):
    paper=get_paper_by_id(db,paper_id)
    if not paper:
        raise HTTPException(status_code=404,detail="No paper found")
    return paper

@router.get(
    "/papers/{paper_id}/search",
    response_model=RetrievalDebugResponse,
)
def search_paper(
    paper_id: int,
    question: str,
    db: Session = Depends(get_db),
):
    return ChatService(db).search_chunks(
        paper_id,
        question,
    )