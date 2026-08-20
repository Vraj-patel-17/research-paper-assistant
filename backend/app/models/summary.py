from __future__ import annotations

import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
if TYPE_CHECKING:
    from app.models.paper import Paper


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)

    paper_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
        ForeignKey("papers.id", ondelete="CASCADE"),
        nullable=False,
    )

    summary_type: Mapped[str] = mapped_column(
        String(30),
        default="standard",
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    paper: Mapped["Paper"] = relationship(
        back_populates="summaries",
    )