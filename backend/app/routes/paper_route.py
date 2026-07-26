from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional
from app.services.paper_services import get_all_papers,get_paper_by_id
from app.schemas.paper import PaperDetailResponse
from fastapi import Depends,HTTPException
router=APIRouter()
@router.get("/papers")
def get_papers(db:Session=Depends(get_db),
    q: Optional[str] = Query(default=None, min_length=2, max_length=200),
    source: Optional[str] = Query(default=None, min_length=2, max_length=50),
    topic:Optional[str]=Query(default=None, min_length=2, max_length=50),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)):
    return get_all_papers(
        db=db,
        q=q,
        source=source,
        topic=topic,
        limit=limit,
        offset=offset,
    )

@router.get("/papers/{paper_id}",response_model=PaperDetailResponse)
def get_paper_from_id(paper_id:int=Path(gt=0),db:Session=Depends(get_db)):
    paper=get_paper_by_id(db,paper_id)
    if not paper:
        raise HTTPException(status_code=404,detail="No paper found")
    return paper

