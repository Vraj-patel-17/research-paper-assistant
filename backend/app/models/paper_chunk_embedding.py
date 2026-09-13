from sqlalchemy import Integer, String, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base 


class PaperChunkEmbedding(Base):
    """Stores only the embedding vector per chunk — never chunk text.

    Chunk text is re-derived from the source PDF on every request (see
    RAGService.prepare_paper); this table exists purely to skip
    re-calling the embedding API when the chunk count hasn't changed.
    """

    __tablename__ = "paper_chunk_embeddings"
    __table_args__ = (
        UniqueConstraint(
            "paper_id", "chunk_index", name="uq_paper_chunk_embedding_index"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paper_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(JSON, nullable=False)