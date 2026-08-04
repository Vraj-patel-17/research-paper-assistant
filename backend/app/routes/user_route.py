from fastapi import APIRouter, Query ,Request
from app.core.rate_limiter import limiter
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.database import get_db
from app.services.user_service import create_user,get_user_by_email,update_username,delete_user,authenticate_user
from app.schemas.user import UserCreate,UserLogin,UserResponse
from app.models.user import User
from fastapi import Depends,HTTPException
from app.core.security import get_current_user
from sqlalchemy.exc import IntegrityError
router=APIRouter()

@router.post("/users",response_model=UserResponse)
@limiter.limit("5/minute")
def create_new_user(request:Request,user: UserCreate,db: Session=Depends(get_db)):
    try:
     return create_user(db,user.username,user.email,user.password)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="Username or email already exists")
@router.get("/users/{emai Integl}")
def get_user(email:EmailStr,db: Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    user=get_user_by_email(db,email)
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    return { "id": user.id,"username":user.username,"email":user.email }
@router.put("/users/{email}")
def update_user(email:EmailStr,new_username:str = Query(min_length=3,max_length=30),db: Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.email != email:
        raise HTTPException(status_code=403,detail="Not allowed",)
    user=update_username(db,email,new_username)
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    return {"id":user.id,"username":user.username}
@router.delete("/users/{email}")
def delete_user_route(email:EmailStr,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    if current_user.email!=email:
        raise HTTPException(status_code=403,detail="Not Allowed")
    user=delete_user(db,email)
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    return { "message":"Deleted"}