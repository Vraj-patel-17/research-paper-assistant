from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends,HTTPException
from app.services.bookmark_services import add_bookmark,remove_bookmark,get_user_bookmarks
from app.core.security import get_current_user
from app.models.user import User
router=APIRouter()
@router.post("/bookmarks/{paper_id}")
def bookmark_paper(paper_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    paper=add_bookmark(db,paper_id,current_user.id)
    if not paper:
        raise HTTPException(status_code=404,detail="Paper not Found")
    return {"message","Paper bookmarked successfully"}
@router.get("/bookmarks")
def get_bookmarks(db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    return get_user_bookmarks(db, current_user.id)
@router.delete("/bookmarks/{paper_id}")
def delete_bookmark(paper_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    deleted = remove_bookmark(db,current_user.id,paper_id,)
    if not deleted:
        raise HTTPException(status_code=404,detail="Bookmark not found")
    return {
        "message": "Bookmark removed successfully"
    }