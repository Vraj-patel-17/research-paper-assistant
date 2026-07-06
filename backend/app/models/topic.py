from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.paper_topic import PaperTopic

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    paper_topics: Mapped[list["PaperTopic"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )