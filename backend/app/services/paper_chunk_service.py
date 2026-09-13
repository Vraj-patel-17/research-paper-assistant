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


async def save_embeddings(
    session: AsyncSession,
    paper_id: str,
    embeddings: list[list[float]],
) -> None:
    await session.execute(
        delete(PaperChunkEmbedding).where(PaperChunkEmbedding.paper_id == paper_id)
    )

    session.add_all(
        [
            PaperChunkEmbedding(paper_id=paper_id, chunk_index=index, embedding=embedding)
            for index, embedding in enumerate(embeddings)
        ]
    )

    await session.commit()