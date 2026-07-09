from __future__ import annotations
import datetime
from sqlalchemy import String,DateTime,func,UniqueConstraint,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bookmark import Bookmark
    from app.models.paper_topic import PaperTopic
    from app.models.topic import Topic
    from app.models.note import Note
class Paper(Base):
    __tablename__="papers"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_paper_source_external_id"),
    )
    id: Mapped[int]=mapped_column(primary_key=True)
    external_id: Mapped[str]=mapped_column(String(50),nullable=False)
    source: Mapped[str]=mapped_column(String(50),nullable=False)
    title: Mapped[str]=mapped_column(String(500),nullable=False)
    authors: Mapped[str]=mapped_column(Text,nullable=False)
    abstract: Mapped[str]=mapped_column(Text)
    pdf_url :Mapped[str]=mapped_column(String(500))
    publication_date:Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),nullable=True)
    created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    bookmarks:Mapped[list["Bookmark"]]=relationship(back_populates="paper",cascade="all,delete-orphan")
    collection_papers = relationship("CollectionPaper",back_populates="paper",cascade="all, delete-orphan",)
    paper_topics: Mapped[list["PaperTopic"]] = relationship(
    back_populates="paper",
    cascade="all, delete-orphan",)
    topics: Mapped[list["Topic"]] = relationship("Topic",
    secondary="paper_topics",
    viewonly=True,)
    notes: Mapped[list["Note"]] = relationship(
    back_populates="paper",
    cascade="all, delete-orphan",)
    summary = relationship(
    "Summary",
    back_populates="paper",
    uselist=False,
    cascade="all, delete-orphan",)