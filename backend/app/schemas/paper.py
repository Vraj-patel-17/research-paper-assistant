from pydantic import BaseModel
from datetime import datetime
from app.schemas.topic import TopicResponse
class PaperDetailResponse(BaseModel):
    id:int
    title:str
    authors:str
    abstract:str
    pdf_url:str
    publication_date:datetime | None
    source: str
    topics: list[TopicResponse]

    class Config:
        from_attributes = True
