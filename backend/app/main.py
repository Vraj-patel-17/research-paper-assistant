from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from services.user_service import create_user,get_user_by_email,update_username,delete_user
from schemas.user import UserCreate
app=FastAPI()
@app.get("/")
async def root():
    return {"message":"Research Paper Assistant API"}
@app.get("/health")
async def health():
    return { "status": "healthy"}
@app.post("/users")
def create_new_user(user: UserCreate,db: Session=Depends(get_db)):
    new_user=create_user(db,user.username,user.email,user.password)
    return {"id":new_user.id,"username":new_user.username,"email":new_user.email}
@app.get("/users/{email}")
def get_user(email:str,db: Session=Depends(get_db)):
    user=get_user_by_email(db,"vraj@gmail.com")
    if not user:
        return {"message":"user not found"}
    return { "id": user.id,"username":user.username,"email":user.email }
@app.put("/users/{email}")
def update_user(email:str,new_username:str,db: Session=Depends(get_db)):
    user=update_username(db,email,new_username)
    if not user:
        return { "message":"User not found"}
    return {"id":user.id,"username":user.username}
@app.delete("/users/{email}")
def delete_user_route(email:str,db:Session=Depends(get_db)):
    user=delete_user(db,email)
    if not user:
        return { "message":"User not found"}
    return { "message":"Deleted"}