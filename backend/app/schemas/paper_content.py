from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class PaperContentResponse(BaseModel):
    id: UUID
    paper_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)