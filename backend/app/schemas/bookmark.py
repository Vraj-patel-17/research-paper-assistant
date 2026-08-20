from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookmarkResponse(BaseModel):
    paper_id: UUID
    title: str
    authors: str
    publication_date: datetime | None
    bookmarked_at: datetime

    model_config = ConfigDict(from_attributes=True)