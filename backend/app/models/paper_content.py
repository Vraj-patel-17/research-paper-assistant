from __future__ import annotations

import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.paper import Paper


class PaperContent(Base):
    __tablename__ = "paper_contents"

    id: Mapped[int] = mapped_column(primary_key=True)

    paper_id: Mapped[int] = mapped_column(
        ForeignKey("papers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    paper: Mapped["Paper"] = relationship(
        back_populates="content",
    )
    chunks = relationship(
    "PaperChunk",
    back_populates="paper_content",
    cascade="all, delete-orphan",
    passive_deletes=True,)