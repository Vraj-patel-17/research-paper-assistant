from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.topic import Topic
from app.models.paper_topic import PaperTopic
from app.services.topic_classifier import classify_topics
class TopicService:
    def __init__(self,db:Session):
        self.db=db
    def assign_topics(self,paper:Paper)-> None:
        topic_names=classify_topics(paper.title,paper.abstract or "")
        if not topic_names:
            return
        topics=(self.db.query(Topic).filter(Topic.name.in_(topic_names)).all())
        for topic in topics:
            self.db.add(PaperTopic(paper_id=paper.id,topic_id=topic.id))
        self.db.commit()
    def list_topics(self):
        return (
            self.db.query(Topic)
            .order_by(Topic.name)
            .all()
        )
    def get_topic_by_slug(self, slug: str):
        return (
            self.db.query(Topic)
            .filter(Topic.slug == slug)
            .first()
        )