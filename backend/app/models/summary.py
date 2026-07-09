from sqlalchemy import Column, Integer, ForeignKey, Text, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)

    paper_id = Column(
        Integer,
        ForeignKey("papers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    summary_text = Column(Text, nullable=False)

    model_name = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    paper = relationship("Paper", back_populates="summary")