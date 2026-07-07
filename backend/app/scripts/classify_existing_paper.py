from app.database import SessionLocal
from app.services.topic_service import TopicService
from app.models.paper import Paper

db = SessionLocal()
topic_service = TopicService(db)
papers = db.query(Paper).all()
for paper in papers:
    topic_service.assign_topics(paper)

db.close()