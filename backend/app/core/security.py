from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
import os
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password : str):
    return pwd_context.hash(password)
def verify_password(password:str,hashed_password:str):
    return pwd_context.verify(password,hashed_password)
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=30)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=401,detail="Could not validate credentials")
    try: 
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,detail="Invalid")
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid")
    user=db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    return user

    
