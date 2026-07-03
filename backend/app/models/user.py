from __future__ import annotations
import datetime
from sqlalchemy import String,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bookmark import Bookmark
class User(Base):
    __tablename__="users"
    
    id: Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str]=mapped_column(String(50),unique=True,nullable=False)
    email: Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    hashed_password: Mapped[str]=mapped_column(String(100))
    created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    bookmarks:Mapped[list["Bookmark"]]=relationship(back_populates="user",cascade="all,delete-orphan")
    collections = relationship("Collection",back_populates="user",cascade="all, delete-orphan",)