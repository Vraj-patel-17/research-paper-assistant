from __future__ import annotations
import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.database import Base


class PaperChunk(Base):
    """Expiring cache of a paper's extracted text + chunk embeddings.
    """

    __tablename__ = "paper_chunks"
    __table_args__ = (
        UniqueConstraint("paper_id", "chunk_index", name="uq_paper_chunk_index"),
    )

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    paper_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papers.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    page: Mapped[int | None] = mapped_column(Integer, nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(
        Vector(settings.embedding_dimensions), nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False
    )