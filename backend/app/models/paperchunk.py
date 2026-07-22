from sqlalchemy import DateTime, ForeignKey, Integer, Text, func,UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector 
from app.database import Base


class PaperChunk(Base):
    __tablename__ = "paper_chunks"
    __table_args__=(UniqueConstraint("paper_content_id","chunk_index",name="uq_paper_content_chunk_index"),)
    id: Mapped[int] = mapped_column(primary_key=True)

    paper_content_id: Mapped[int] = mapped_column(
        ForeignKey("paper_contents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    section: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    embedding = mapped_column(Vector(3072), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    paper_content = relationship(
        "PaperContent",
        back_populates="chunks",
    )