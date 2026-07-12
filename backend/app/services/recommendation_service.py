from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.paper_topic import PaperTopic
from app.services.paper_services import get_paper_by_id
class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_recommendations(
    self,
    paper_id: int,
    limit: int = 10) -> list[Paper]:
        paper = get_paper_by_id(self.db,paper_id)
        topic_ids = (self.db.query(PaperTopic.topic_id).filter(PaperTopic.paper_id == paper_id).all())
        topic_ids = [topic_id for (topic_id,) in topic_ids]
        if not topic_ids:
            return []
        recommendations = (
        self.db.query(Paper)
        .join(PaperTopic, Paper.id == PaperTopic.paper_id)
        .filter(
            PaperTopic.topic_id.in_(topic_ids),
            Paper.id != paper_id,
        )
        .group_by(Paper.id)
        .order_by(
            desc(func.count(PaperTopic.topic_id)),
            desc(Paper.publication_date),
        )
        .limit(limit)
        .all())
        return recommendations