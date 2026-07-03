from __future__ import annotations
import datetime
from sqlalchemy import DateTime,func,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.paper import Paper
class Bookmark(Base):
    __tablename__="bookmarks"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    paper_id:Mapped[int]=mapped_column(ForeignKey("papers.id",ondelete="CASCADE"))
    bookmarked_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="bookmarks")
    paper: Mapped["Paper"] = relationship(back_populates="bookmarks")
    __table_args__ = (UniqueConstraint("user_id", "paper_id",name="uq_user_paper_bookmark"),)