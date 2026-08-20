from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
class CollectionPaper(Base):
    __tablename__ = "collection_papers"
    __table_args__ = (UniqueConstraint("collection_id","paper_id",name="uq_collection_paper",),)

    id: Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    collection_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("collections.id", ondelete="CASCADE"),nullable=False,)
    paper_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("papers.id", ondelete="CASCADE"),nullable=False,)
    collection = relationship("Collection",back_populates="collection_papers",)
    paper = relationship("Paper",back_populates="collection_papers",)