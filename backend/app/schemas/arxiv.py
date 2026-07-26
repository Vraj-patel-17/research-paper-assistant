from datetime import datetime

from pydantic import BaseModel,AnyUrl

class ArxivPaper(BaseModel):
    external_id: str
    title: str
    abstract: str
    authors: list[str]
    published_at: datetime
    pdf_url: AnyUrl | None = None
    categories: list[str]