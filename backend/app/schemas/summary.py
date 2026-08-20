from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class SummaryResponse(BaseModel):
    id: UUID
    paper_id: UUID
    summary_type: str 
    model_name: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)