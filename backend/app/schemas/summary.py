from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SummaryBase(BaseModel):
    summary_text: str

class SummaryCreate(SummaryBase):
    pass

class SummaryResponse(SummaryBase):
    id: int
    paper_id: int
    model_name: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)