from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate
from sqlalchemy import select
from app.models.paper import Paper
from app.models.collection_paper import CollectionPaper
from app.schemas.collection_paper import AddPaperToCollection
from uuid import UUID

async def create_collection(db: AsyncSession, user_id: UUID, collection_data: CollectionCreate) -> Collection:
    collection = Collection(name=collection_data.name, description=collection_data.description, user_id=user_id)
    db.add(collection)
    try:
        await db.commit()
        await db.refresh(collection)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A collection with this name already exists.",
        )
    return collection

async def get_user_collections(db: AsyncSession, user_id: UUID) -> list[Collection]:
    result = await db.execute(select(Collection).where(Collection.user_id == user_id))
    return result.scalars().all()

async def get_collection_by_id(db: AsyncSession, collection_id: UUID, user_id: UUID) -> Collection:
    result = await db.execute(
        select(Collection).where(Collection.id == collection_id, Collection.user_id == user_id)
    )
    collection = result.scalar_one_or_none()
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found.",
        )
    return collection

async def delete_collection(db: AsyncSession, collection_id: UUID, user_id: UUID):
    collection = await get_collection_by_id(db, collection_id, user_id)
    await db.delete(collection)
    await db.commit()

async def add_paper_to_collection(
    db: AsyncSession,
    collection_id: UUID,
    user_id: UUID,
    data: AddPaperToCollection,
):
    collection = await get_collection_by_id(db, collection_id, user_id)
    paper = await db.get(Paper, data.paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    exists = await db.scalar(
        select(CollectionPaper).where(
            CollectionPaper.collection_id == collection.id,
            CollectionPaper.paper_id == data.paper_id,
        )
    )
    if exists:
        raise HTTPException(status_code=409, detail="Paper already exists in collection")

    collection_paper = CollectionPaper(
        collection_id=collection.id,
        paper_id=data.paper_id,
    )
    db.add(collection_paper)
    await db.commit()

async def get_collection_papers(
    db: AsyncSession,
    collection_id: UUID,
    user_id: UUID,
):
    await get_collection_by_id(db, collection_id, user_id)

    result = await db.execute(
        select(Paper)
        .options(selectinload(Paper.topics))
        .join(CollectionPaper)
        .where(CollectionPaper.collection_id == collection_id)
    )
    return result.scalars().all()

async def remove_paper_from_collection(
    db: AsyncSession,
    collection_id: UUID,
    paper_id: UUID,
    user_id: UUID,
):
    await get_collection_by_id(db, collection_id, user_id)

    collection_paper = await db.scalar(
        select(CollectionPaper).where(
            CollectionPaper.collection_id == collection_id,
            CollectionPaper.paper_id == paper_id,
        )
    )

    if not collection_paper:
        raise HTTPException(status_code=404, detail="Paper not found in collection")

    await db.delete(collection_paper)
    await db.commit()