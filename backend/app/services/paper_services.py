from app.models.paper import Paper
from sqlalchemy.orm import Session
def get_all_papers(db:Session):
    return (db.query(Paper).all())
def get_paper_by_id(db:Session,paper_id):
     return ( db.query(Paper).filter(Paper.id==paper_id).first())
def search_papers(db:Session,search_term):
     return(db.query(Paper).filter(Paper.title.ilike(f"%{search_term}%")).all())