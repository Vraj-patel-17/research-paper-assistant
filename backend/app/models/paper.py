import datetime
from sqlalchemy import String,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from database import Base
class Paper(Base):
    __tablename__="papers"
    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(100),nullable=False)
    authors: Mapped[str]=mapped_column(String(100),nullable=False)
    abstract: Mapped[str]=mapped_column(String(5000))
    pdf_url :Mapped[str]=mapped_column(String(500))
    publication_date:Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),nullable=True)
    created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    