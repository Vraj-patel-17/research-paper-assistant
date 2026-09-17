from app.models.bookmark import Bookmark
from app.models.paper import Paper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

async def add_bookmark(db: AsyncSession, paper_id: UUID, user_id: UUID):
    paper = await db.get(Paper, paper_id)
    if not paper:
        return None
    result = await db.execute(
        select(Bookmark).where(Bookmark.user_id == user_id, Bookmark.paper_id == paper_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    bookmark = Bookmark(user_id=user_id, paper_id=paper_id)
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return bookmark

async def get_user_bookmarks(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Bookmark).where(Bookmark.user_id == user_id))
    return result.scalars().all()

async def remove_bookmark(db: AsyncSession, user_id: UUID, paper_id: UUID):
    result = await db.execute(
        select(Bookmark).where(Bookmark.user_id == user_id, Bookmark.paper_id == paper_id)
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        return False
    await db.delete(bookmark)
    await db.commit()
    return True