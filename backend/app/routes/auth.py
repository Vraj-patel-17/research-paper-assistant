from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from fastapi import Depends,HTTPException
from app.core.security import create_access_token,get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import authenticate_user
router=APIRouter()
@router.post('/login')
def authenticate(form_data:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(get_db)):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token=create_access_token({"sub":user.email})
    return {"access_token":token,"token_type":"bearer"}
@router.get("/me",response_model=UserResponse)
def get_me(current_user:User=Depends(get_current_user)):
    return {"id":current_user.id,"email":current_user.email}