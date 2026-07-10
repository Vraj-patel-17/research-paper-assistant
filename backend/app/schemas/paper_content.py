from datetime import datetime

from pydantic import BaseModel, ConfigDict

class PaperContentResponse(BaseModel):
    id: int
    paper_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)