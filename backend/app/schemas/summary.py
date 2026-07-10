from datetime import datetime

from pydantic import BaseModel, ConfigDict

class SummaryResponse(BaseModel):
    id: int
    paper_id: int
    summary_type: str
    model_name: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)