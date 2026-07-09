from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class PaperSection(Base):
    __tablename__ = "paper_sections"

    id = Column(Integer, primary_key=True, index=True)

    paper_content_id = Column(
        Integer,
        ForeignKey("paper_contents.id", ondelete="CASCADE"),
        nullable=False,
    )

    section_name = Column(
        String,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    order_index = Column(
        Integer,
        nullable=False,
    )

    paper_content = relationship(
        "PaperContent",
        back_populates="sections",
    )