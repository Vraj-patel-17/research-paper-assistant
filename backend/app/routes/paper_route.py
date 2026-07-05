from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional
from app.services.paper_services import get_all_papers,get_paper_by_id
from fastapi import Depends,HTTPException
router=APIRouter()
@router.get("/papers")
def get_papers(db:Session=Depends(get_db),q: Optional[str] = None,source: Optional[str] = None,limit: int = 20,offset: int = 0,):
    return get_all_papers(
        db=db,
        q=q,
        source=source,
        limit=limit,
        offset=offset,
    )

@router.get("/papers/{paper_id}")
def get_paper_from_id(paper_id:int,db:Session=Depends(get_db)):
    paper=get_paper_by_id(db,paper_id)
    if not paper:
        raise HTTPException(status_code=404,detail="No paper found")
    return paper