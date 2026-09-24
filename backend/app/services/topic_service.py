from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.paper import Paper
from app.models.topic import Topic
from app.models.paper_topic import PaperTopic
from app.services.topic_classifier import classify_topics


class TopicService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assign_topics(self, paper: Paper) -> None:
        topic_names = classify_topics(paper.title, paper.abstract or "")
        if not topic_names:
            return

        result = await self.db.execute(
            select(Topic).where(Topic.name.in_(topic_names))
        )
        topics = result.scalars().all()

        for topic in topics:
            exists_result = await self.db.execute(
                select(PaperTopic).where(
                    PaperTopic.paper_id == paper.id,
                    PaperTopic.topic_id == topic.id,
                )
            )
            exists = exists_result.scalar_one_or_none()

            if not exists:
                self.db.add(
                    PaperTopic(
                        paper_id=paper.id,
                        topic_id=topic.id,
                    )
                )

        await self.db.commit()

    async def list_topics(self):
        result = await self.db.execute(
            select(Topic).order_by(Topic.name)
        )
        return result.scalars().all()

    async def get_topic_by_slug(self, slug: str):
        result = await self.db.execute(
            select(Topic).where(Topic.slug == slug)
        )
        return result.scalar_one_or_none()