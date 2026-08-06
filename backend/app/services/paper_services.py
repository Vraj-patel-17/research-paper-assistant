from app.models.paper import Paper
from app.models.paper_topic import PaperTopic
from app.models.topic import Topic
from sqlalchemy.orm import Session
from sqlalchemy import or_
def get_all_papers(db:Session,q:str|None=None,source:str |None=None,topic: str | None = None,sort: str = "latest",limit:int=20,offset:int=0):
     query=db.query(Paper)
     if q:
         search=f"%{q}%"
         query=query.filter(
              or_(Paper.title.ilike(search),
                  Paper.abstract.ilike(search),)
         )
     if source:
          query=query.filter(Paper.source==source)
     if topic:
          query=(query.join(PaperTopic,Paper.id==PaperTopic.paper_id).join(Topic,PaperTopic.topic_id==Topic.id).filter(Topic.slug==topic))
     if sort=="latest":
          query = query.order_by(Paper.publication_date.desc())
     elif sort == "oldest":
          query = query.order_by(Paper.publication_date.asc())

     elif sort == "title":
          query = query.order_by(Paper.title.asc())
     total = query.count()
     papers=(query.offset(offset).limit(limit).all())
     return {
          "items":papers,
          "total": total,
          "limit": limit,
          "offset": offset,
          "has_next": offset + limit < total,
     }

def get_paper_by_id(db:Session,paper_id):
     return ( db.query(Paper).filter(Paper.id==paper_id).first())
