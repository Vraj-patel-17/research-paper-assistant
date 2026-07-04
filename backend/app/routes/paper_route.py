from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.paper_services import get_all_papers,get_paper_by_id,search_papers
from fastapi import Depends,HTTPException
router=APIRouter()
@router.get("/papers")
def get_papers(db:Session=Depends(get_db),):
    papers=get_all_papers(db)
    if not papers:
        return []
    return papers
@router.get("/papers/search")
def search_for_papers(q:str,db:Session=Depends(get_db)):
    papers=search_papers(db,q)
    if not papers:
        return []
    return papers
@router.get("/papers/{paper_id}")
def get_paper_from_id(paper_id:int,db:Session=Depends(get_db)):
    paper=get_paper_by_id(db,paper_id)
    if not paper:
        raise HTTPException(status_code=404,detail="No paper found")
    return paper