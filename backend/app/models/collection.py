from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
class Collection(Base):
    __tablename__ = "collections"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_collection_name"),)
    id: Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id", ondelete="CASCADE"),nullable=False,)

    user = relationship("User",back_populates="collections",)
    collection_papers = relationship("CollectionPaper",back_populates="collection",cascade="all, delete-orphan",)