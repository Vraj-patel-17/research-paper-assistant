from app.models.bookmark import Bookmark
from app.models.paper import Paper
from sqlalchemy.orm import Session
from uuid import UUID
def add_bookmark(db:Session,paper_id:UUID,user_id:UUID):
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
    
def get_user_bookmarks(db:Session,user_id:UUID):
    return (db.query(Bookmark).filter(Bookmark.user_id==user_id).all())

def remove_bookmark(db: Session, user_id: UUID, paper_id: UUID):
    bookmark = (db.query(Bookmark).filter(Bookmark.user_id == user_id,Bookmark.paper_id == paper_id).first())

    if not bookmark:
        return False
    db.delete(bookmark)
    db.commit()
    
    return True
