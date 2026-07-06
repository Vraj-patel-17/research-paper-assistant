from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.paper import Paper
    from app.models.topic import Topic

class PaperTopic(Base):
    __tablename__ = "paper_topics"

    __table_args__ = (
        UniqueConstraint(
            "paper_id",
            "topic_id",
            name="uq_paper_topic",
        ),
    )
    paper_id: Mapped[int] = mapped_column(
        ForeignKey("papers.id", ondelete="CASCADE"),
        primary_key=True,
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"),
        primary_key=True,
    )
    paper: Mapped["Paper"] = relationship(
        back_populates="paper_topics"
    )
    topic: Mapped["Topic"] = relationship(
        back_populates="paper_topics"
    )