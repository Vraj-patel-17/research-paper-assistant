from app.models.paper import Paper
from sqlalchemy.orm import Session
from sqlalchemy import or_
def get_all_papers(db:Session,q:str|None=None,source:str |None=None,limit:int=20,offset:int=0):
     query=db.query(Paper)
     if q:
         search=f"%{q}%"
         query=query.filter(
              or_(Paper.title.ilike(search),
                  Paper.abstract.ilike(search),)
         )
     if source:
          query=query.filter(Paper.source==source)
     query = query.order_by(Paper.publication_date.desc())

     return query.offset(offset).limit(limit).all()

def get_paper_by_id(db:Session,paper_id):
     return ( db.query(Paper).filter(Paper.id==paper_id).first())
