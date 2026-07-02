from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BookmarkResponse(BaseModel):
    paper_id: int
    title: str
    authors: str
    publication_date: datetime | None
    bookmarked_at: datetime

    model_config = ConfigDict(from_attributes=True)