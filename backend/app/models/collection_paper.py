from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class CollectionPaper(Base):
    __tablename__ = "collection_papers"
    __table_args__ = (UniqueConstraint("collection_id","paper_id",name="uq_collection_paper",),)

    id: Mapped[int] = mapped_column(primary_key=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id", ondelete="CASCADE"),nullable=False,)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"),nullable=False,)
    collection = relationship("Collection",back_populates="collection_papers",)
    paper = relationship("Paper",back_populates="collection_papers",)