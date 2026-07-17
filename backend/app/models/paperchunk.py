from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PaperChunk(Base):
    __tablename__ = "paper_chunks"

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
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    paper_content = relationship(
        "PaperContent",
        back_populates="chunks",
    )