from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from fastapi import Depends,HTTPException
from app.services.bookmark_services import add_bookmark,remove_bookmark,get_user_bookmarks
from app.core.security import get_current_user
from app.models.user import User
from uuid import UUID
router=APIRouter()
@router.post("/bookmarks/{paper_id}")
async def bookmark_paper(paper_id:UUID,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    paper=await add_bookmark(db,paper_id,current_user.id)
    if not paper:
        raise HTTPException(status_code=404,detail="Paper not Found")
    return {"message":"Paper bookmarked successfully"}
@router.get("/bookmarks")
async def get_bookmarks(db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await get_user_bookmarks(db, current_user.id)
@router.delete("/bookmarks/{paper_id}")
async def delete_bookmark(paper_id:UUID,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    deleted = await remove_bookmark(db,current_user.id,paper_id,)
    if not deleted:
        raise HTTPException(status_code=404,detail="Bookmark not found")
    return {
        "message": "Bookmark removed successfully"
    }