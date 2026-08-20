from __future__ import annotations
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.paper import Paper


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    paper_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
        ForeignKey("papers.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="notes")

    paper: Mapped["Paper"] = relationship(back_populates="notes")