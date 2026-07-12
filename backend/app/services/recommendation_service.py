from sqlalchemy import func, desc
from sqlalchemy.orm import Session,selectinload
from app.models.paper import Paper
from app.models.paper_topic import PaperTopic
from app.services.paper_services import get_paper_by_id
from app.schemas.recommendation import RecommendationResponse
class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_recommendations(
    self,
    paper_id: int,
    limit: int = 10) -> list[RecommendationResponse]:
        paper = get_paper_by_id(self.db,paper_id)
        topic_ids = (self.db.query(PaperTopic.topic_id).filter(PaperTopic.paper_id == paper_id).all())
        topic_ids = [topic_id for (topic_id,) in topic_ids]
        if not topic_ids:
            return []
        current_topics = (
        self.db.query(PaperTopic).options(selectinload(PaperTopic.topic))
        .filter(PaperTopic.paper_id == paper_id)
        .all())

        current_topic_map = {topic.topic_id: topic.topic.name for topic in current_topics}
        recommendations = (
        self.db.query(Paper).options(
        selectinload(Paper.paper_topics)
        .selectinload(PaperTopic.topic))
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
        response=[]
        for paper in recommendations:
            shared_topics=[]
            for paper_topic in paper.paper_topics:
                if paper_topic.topic_id in current_topic_map:
                    shared_topics.append(current_topic_map[paper_topic.topic_id ])
            response.append(RecommendationResponse(paper=paper,shared_topics=shared_topics,shared_topic_count=len(shared_topics),reason=f"Shares {len(shared_topics)} topic(s) with the current paper."))
        return response
       # return recommendations