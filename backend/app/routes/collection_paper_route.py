from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends,HTTPException,status
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.collection_paper import AddPaperToCollection
from app.schemas.paper import PaperResponse
from app.services.collection_services import add_paper_to_collection,get_collection_papers,remove_paper_from_collection
router=APIRouter()

@router.post("/collections/{collection_id}/papers",status_code=status.HTTP_201_CREATED)
def add_paper(collection_id:int,data:AddPaperToCollection,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    add_paper_to_collection(db=db,collection_id=collection_id,user_id=current_user.id,data=data)
    return {"message":"Paper added to collection successfully"}
@router.get("/collections/{collection_id}/papers",response_model=list[PaperResponse])

def get_papers(collection_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_collection_papers(db=db,collection_id=collection_id,user_id=current_user.id)

@router.delete("/collections/{collection_id}/papers/{paper_id}",status_code=status.HTTP_204_NO_CONTENT)
def remove_paper(collection_id:int,paper_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    remove_paper_from_collection(
        db=db,
        collection_id=collection_id,
        paper_id=paper_id,
        user_id=current_user.id
    )