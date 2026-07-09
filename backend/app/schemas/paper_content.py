from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaperContentResponse(BaseModel):
    id: int
    paper_id: int
    page_count: int | None
    extraction_status: str
    full_text: str
    extracted_at: datetime

    model_config = ConfigDict(from_attributes=True)