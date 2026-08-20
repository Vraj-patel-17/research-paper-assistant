from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
if TYPE_CHECKING:
    from app.models.paper_topic import PaperTopic
    from app.models.paper import Paper


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    slug:Mapped[str]= mapped_column(String(100), unique=True, nullable=False, index=True)
    paper_topics: Mapped[list["PaperTopic"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    papers: Mapped[list["Paper"]] = relationship("Paper",
    secondary="paper_topics",
    viewonly=True,)