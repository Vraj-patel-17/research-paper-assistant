from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import create_user,get_user_by_email,update_username,delete_user,authenticate_user
from app.schemas.user import UserCreate,UserLogin,UserResponse
from app.models.user import User
from fastapi import Depends,HTTPException
from app.core.security import get_current_user
router=APIRouter()

@router.post("/users")
def create_new_user(user: UserCreate,db: Session=Depends(get_db)):
    new_user=create_user(db,user.username,user.email,user.password)
    return {"id":new_user.id,"username":new_user.username,"email":new_user.email}
@router.get("/users/{email}")
def get_user(email:str,db: Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    user=get_user_by_email(db,"vraj@gmail.com")
    if not user:
        raise HTTPException(status_code=401,detail="User not Found")
    return { "id": user.id,"username":user.username,"email":user.email }
@router.put("/users/{email}")
def update_user(email:str,new_username:str,db: Session=Depends(get_db)):
    user=update_username(db,email,new_username)
    if not user:
        raise HTTPException(status_code=401,detail="User not Found")
    return {"id":user.id,"username":user.username}
@router.delete("/users/{email}")
def delete_user_route(email:str,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    if current_user.email!=email:
        raise HTTPException(status_code=403,detail="Not Allowed")
    user=delete_user(db,email)
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    return { "message":"Deleted"}