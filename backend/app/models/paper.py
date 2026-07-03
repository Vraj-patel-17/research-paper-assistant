from __future__ import annotations
import datetime
from sqlalchemy import String,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bookmark import Bookmark
class Paper(Base):
    __tablename__="papers"
    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(100),nullable=False)
    authors: Mapped[str]=mapped_column(String(100),nullable=False)
    abstract: Mapped[str]=mapped_column(String(5000))
    pdf_url :Mapped[str]=mapped_column(String(500))
    publication_date:Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),nullable=True)
    created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    bookmarks:Mapped[list["Bookmark"]]=relationship(back_populates="paper",cascade="all,delete-orphan")
    