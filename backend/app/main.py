from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import create_user,get_user_by_email,update_username,delete_user,authenticate_user
from app.schemas.user import UserCreate,UserLogin,UserResponse
from app.core.security import create_access_token,get_current_user
from app.services.paper_services import get_all_papers,get_paper_by_id,search_papers
from app.services.bookmark_services import add_bookmark,remove_bookmark,get_user_bookmarks
from app.models.user import User
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
def get_user(email:str,db: Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    user=get_user_by_email(db,"vraj@gmail.com")
    if not user:
        raise HTTPException(status_code=401,detail="User not Found")
    return { "id": user.id,"username":user.username,"email":user.email }
@app.put("/users/{email}")
def update_user(email:str,new_username:str,db: Session=Depends(get_db)):
    user=update_username(db,email,new_username)
    if not user:
        raise HTTPException(status_code=401,detail="User not Found")
    return {"id":user.id,"username":user.username}
@app.delete("/users/{email}")
def delete_user_route(email:str,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    if current_user.email!=email:
        raise HTTPException(status_code=403,detail="Not Allowed")
    user=delete_user(db,email)
    if not user:
        raise HTTPException(status_code=404,detail="User not Found")
    return { "message":"Deleted"}
@app.post('/login')
def authenticate(form_data:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(get_db)):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token=create_access_token({"sub":user.email})
    return {"access_token":token,"token_type":"bearer"}
@app.get("/me",response_model=UserResponse)
def get_me(current_user:User=Depends(get_current_user)):
    return {"id":current_user.id,"email":current_user.email}
@app.get("/papers")
def get_papers(db:Session=Depends(get_db),):
    papers=get_all_papers(db)
    if not papers:
        return []
    return papers
@app.get("/papers/search")
def search_for_papers(q:str,db:Session=Depends(get_db)):
    papers=search_papers(db,q)
    if not papers:
        return []
    return papers
@app.get("/papers/{paper_id}")
def get_paper_from_id(paper_id:int,db:Session=Depends(get_db)):
    paper=get_paper_by_id(db,paper_id)
    if not paper:
        raise HTTPException(status_code=404,detail="No paper found")
    return paper
@app.post("/bookmarks/{paper_id}")
def bookmark_paper(paper_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    paper=add_bookmark(db,paper_id,current_user.id)
    if not paper:
        raise HTTPException(status_code=404,detail="Paper not Found")
    return {"message","Paper bookmarked successfully"}
@app.get("/bookmarks")
def get_bookmarks(db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    return get_user_bookmarks(db, current_user.id)
@app.delete("/bookmarks/{paper_id}")
def delete_bookmark(paper_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    deleted = remove_bookmark(db,current_user.id,paper_id,)
    if not deleted:
        raise HTTPException(status_code=404,detail="Bookmark not found")
    return {
        "message": "Bookmark removed successfully"
    }