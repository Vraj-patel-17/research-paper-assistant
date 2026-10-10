import datetime
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.paper_chunk import PaperChunk
from app.schemas.rag import RetrievedChunk


async def purge_expired_chunks(session: AsyncSession) -> int:
    """Deletes cached chunks past their expiry. Cheap (indexed), so it runs
    opportunistically before each ingestion instead of needing a scheduler."""
    result = await session.execute(
        delete(PaperChunk).where(PaperChunk.expires_at < func.now())
    )
    await session.commit()
    return result.rowcount or 0


async def has_fresh_chunks(session: AsyncSession, paper_id: UUID) -> bool:
    result = await session.execute(
        select(PaperChunk.id)
        .where(
            PaperChunk.paper_id == paper_id,
            PaperChunk.expires_at > func.now(),
        )
        .limit(1)
    )
    return result.first() is not None


async def replace_chunks(
    session: AsyncSession,
    paper_id: UUID,
    rows: list[tuple[int | None, str, list[float]]],
) -> None:
    """Atomically swaps a paper's cached chunks for a fresh set.

    rows: (page, text, embedding) per chunk, in chunk order.
    """
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=settings.chunk_cache_ttl_days
    )

    await session.execute(delete(PaperChunk).where(PaperChunk.paper_id == paper_id))
    session.add_all(
        [
            PaperChunk(
                paper_id=paper_id,
                chunk_index=index,
                page=page,
                text=text,
                embedding=embedding,
                expires_at=expires_at,
            )
            for index, (page, text, embedding) in enumerate(rows)
        ]
    )
    await session.commit()


async def search_chunks(
    session: AsyncSession,
    paper_id: UUID,
    query_embedding: list[float],
    top_k: int,
) -> list[RetrievedChunk]:
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    distance = PaperChunk.embedding.cosine_distance(query_embedding)

    result = await session.execute(
        select(PaperChunk, distance.label("distance"))
        .where(
            PaperChunk.paper_id == paper_id,
            PaperChunk.expires_at > func.now(),
        )
        .order_by(distance)
        .limit(top_k)
    )

    return [
        RetrievedChunk(text=chunk.text, score=1.0 - float(dist), page=chunk.page)
        for chunk, dist in result.all()
    ]