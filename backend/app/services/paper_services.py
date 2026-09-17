from app.models.paper import Paper
from app.models.paper_topic import PaperTopic
from app.models.topic import Topic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, func,Select
from sqlalchemy.orm import selectinload
from uuid import UUID

async def get_all_papers(db: AsyncSession, q: str | None = None, source: str | None = None, topic: str | None = None, sort: str = "latest", limit: int = 20, offset: int = 0):
    stmt = select(Paper)

    if q:
        search = f"%{q}%"
        stmt = stmt.where(
            or_(Paper.title.ilike(search), Paper.abstract.ilike(search))
        )
    if source:
        stmt = stmt.where(Paper.source == source)
    if topic:
        stmt = (
            stmt.join(PaperTopic, Paper.id == PaperTopic.paper_id)
            .join(Topic, PaperTopic.topic_id == Topic.id)
            .where(Topic.slug == topic)
        )
    if sort == "latest":
        stmt = stmt.order_by(Paper.publication_date.desc())
    elif sort == "oldest":
        stmt = stmt.order_by(Paper.publication_date.asc())
    elif sort == "title":
        stmt = stmt.order_by(Paper.title.asc())

    count_stmt = select(func.count()).select_from(
        stmt.with_only_columns(Paper.id).order_by(None).subquery()
    )
    total = (await db.execute(count_stmt)).scalar_one()

    result = await db.execute(stmt.offset(offset).limit(limit))
    papers = result.scalars().all()

    return {
        "items": papers,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_next": offset + limit < total,
    }

async def get_paper_by_id(db: AsyncSession, paper_id: UUID):
    result = await db.execute(
        select(Paper).where(Paper.id==paper_id)
        .options(selectinload(Paper.topics),selectinload(Paper.summary),)
        
    )
    return result.scalar_one_or_none()