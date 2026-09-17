from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.paper_chunk_embedding import PaperChunkEmbedding


async def get_stored_embeddings(
    session: AsyncSession,
    paper_id: str,
) -> list[list[float]]:
    """Returns embeddings ordered by chunk_index, or [] if nothing cached."""
    result = await session.execute(
        select(PaperChunkEmbedding)
        .where(PaperChunkEmbedding.paper_id == paper_id)
        .order_by(PaperChunkEmbedding.chunk_index)
    )
    rows = result.scalars().all()
    return [row.embedding for row in rows]


async def clear_embeddings(session: AsyncSession, paper_id: str) -> None:
    """Call once before starting a fresh ingestion, to wipe any partial
    leftovers from a previous failed attempt."""
    await session.execute(
        delete(PaperChunkEmbedding).where(PaperChunkEmbedding.paper_id == paper_id)
    )
    await session.commit()


async def save_partial_embeddings(
    session: AsyncSession,
    paper_id: str,
    start_index: int,
    embeddings: list[list[float]],
) -> None:
    """Appends one batch's embeddings, indexed starting at start_index.
    Does NOT delete existing rows — call clear_embeddings() once before
    the batch loop starts instead."""
    session.add_all(
        [
            PaperChunkEmbedding(
                paper_id=paper_id,
                chunk_index=start_index + offset,
                embedding=embedding,
            )
            for offset, embedding in enumerate(embeddings)
        ]
    )
    await session.commit()


async def save_embeddings(
    session: AsyncSession,
    paper_id: str,
    embeddings: list[list[float]],
) -> None:
    """Kept for backward compatibility / non-incremental callers."""
    await clear_embeddings(session, paper_id)
    await save_partial_embeddings(session, paper_id, 0, embeddings)