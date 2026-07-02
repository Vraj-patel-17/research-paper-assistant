from app.models.bookmark import Bookmark
from app.models.paper import Paper
from sqlalchemy.orm import Session
def add_bookmark(db:Session,paper_id:int,user_id:int):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        return None
    existing = (db.query(Bookmark).filter(Bookmark.user_id == user_id,Bookmark.paper_id == paper_id).first())
    if existing:
        return existing
    bookmark = Bookmark(user_id=user_id,paper_id=paper_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark
    
def get_user_bookmarks(db:Session,user_id:int):
    return (db.query(Bookmark).filter(Bookmark.user_id==user_id).all())

def remove_bookmark(db: Session, user_id: int, paper_id: int):
    bookmark = (db.query(Bookmark).filter(Bookmark.user_id == user_id,Bookmark.paper_id == paper_id).first())

    if not bookmark:
        return False
    db.delete(bookmark)
    db.commit()
    
    return True
