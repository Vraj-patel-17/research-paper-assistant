from sqlalchemy import func, desc, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.paper import Paper
from app.models.paper_topic import PaperTopic
from app.services.paper_services import get_paper_by_id
from app.schemas.recommendation import RecommendationResponse
from app.core.logging import get_logger
logger = get_logger(__name__)

class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recommendations(self, paper_id, limit: int = 10) -> list[RecommendationResponse]:
        try:
            logger.info("Generating recommendations for paper %s", paper_id)
            paper = await get_paper_by_id(self.db, paper_id)
            if not paper:
                return []

            topic_ids_result = await self.db.execute(
                select(PaperTopic.topic_id).where(PaperTopic.paper_id == paper_id)
            )
            topic_ids = [topic_id for (topic_id,) in topic_ids_result.all()]
            if not topic_ids:
                return []

            current_topics_result = await self.db.execute(
                select(PaperTopic)
                .options(selectinload(PaperTopic.topic))
                .where(PaperTopic.paper_id == paper_id)
            )
            current_topics = current_topics_result.scalars().all()
            current_topic_map = {topic.topic_id: topic.topic.name for topic in current_topics}

            recommendations_result = await self.db.execute(
                select(Paper)
                .options(selectinload(Paper.paper_topics).selectinload(PaperTopic.topic))
                .join(PaperTopic, Paper.id == PaperTopic.paper_id)
                .where(
                    PaperTopic.topic_id.in_(topic_ids),
                    Paper.id != paper_id,
                )
                .group_by(Paper.id)
                .order_by(
                    desc(func.count(PaperTopic.topic_id)),
                    desc(Paper.publication_date),
                )
                .limit(limit)
            )
            recommendations = recommendations_result.scalars().all()

            response = []
            for rec_paper in recommendations:
                shared_topics = []
                for paper_topic in rec_paper.paper_topics:
                    if paper_topic.topic_id in current_topic_map:
                        shared_topics.append(current_topic_map[paper_topic.topic_id])
                response.append(
                    RecommendationResponse(
                        paper=rec_paper,
                        shared_topics=shared_topics,
                        shared_topic_count=len(shared_topics),
                        reason=f"Shares {len(shared_topics)} topic(s) with the current paper.",
                    )
                )
            logger.debug("Found %d candidate recommendations", len(response))
            return response
        except Exception:
            logger.exception(
                "Failed to generate recommendations for paper %s",
                paper_id,
            )
            raise