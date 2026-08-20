from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
class NoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str = Field(
        min_length=1,
        max_length=10000,
    )

class NoteUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str = Field(
            min_length=1,
            max_length=10000,
        )

class NoteResponse(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    paper_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True