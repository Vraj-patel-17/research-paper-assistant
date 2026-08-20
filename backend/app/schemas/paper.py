from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

from app.schemas.topic import TopicResponse


class PaperDetailResponse(BaseModel):
    id: UUID
    title: str
    authors: str
    abstract: str
    pdf_url: str
    publication_date: datetime | None
    source: str
    topics: list[TopicResponse]

    model_config = ConfigDict(from_attributes=True)


class PaperResponse(BaseModel):
    id: UUID
    title: str
    authors: str
    publication_date: datetime | None
    source: str

    model_config = ConfigDict(from_attributes=True)


class PaperListResponse(BaseModel):
    items: list[PaperResponse]
    total: int
    limit: int
    offset: int
    has_next: bool