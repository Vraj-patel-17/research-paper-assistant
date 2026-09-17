from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from fastapi import Depends,HTTPException,status
from app.schemas.collection import CollectionCreate,CollectionResponse
from app.services.collection_services import create_collection,get_collection_by_id,get_user_collections,delete_collection
from app.core.security import get_current_user
from app.models.user import User
from uuid import UUID
router=APIRouter()
@router.post("/collections",response_model=CollectionResponse,status_code=status.HTTP_201_CREATED,)
async def create_new_collection(collection: CollectionCreate,db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),):
    return await create_collection(db=db,user_id=current_user.id,collection_data=collection,)
@router.get("/collections",response_model=list[CollectionResponse],)
async def get_collections(db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await get_user_collections(db=db,user_id=current_user.id,)
@router.get("/collections/{collection_id}",response_model=CollectionResponse,)
async def get_collection(collection_id:UUID,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await get_collection_by_id(db=db,collection_id=collection_id,user_id=current_user.id,)
@router.delete("/collections/{collection_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def remove_collection(collection_id:UUID,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    await delete_collection(
        db=db,collection_id=collection_id,user_id=current_user.id,)