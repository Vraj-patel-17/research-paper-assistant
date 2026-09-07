from uuid import UUID
from pydantic import BaseModel

class SummaryResponse(BaseModel):
    paper_id: UUID
    summary: str 
    