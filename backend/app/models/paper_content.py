from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text ,String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PaperContent(Base):
    __tablename__ = "paper_contents"

    id = Column(Integer, primary_key=True, index=True)

    paper_id = Column(
        Integer,
        ForeignKey("papers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    full_text = Column(Text, nullable=False)
    page_count = Column(Integer, nullable=True)
    extraction_status = Column(
        String,
        nullable=False,
        default="completed",
    )
    extracted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    paper = relationship(
        "Paper",
        back_populates="content",
    )
    sections = relationship(
    "PaperSection",
    back_populates="paper_content",
    cascade="all, delete-orphan",)