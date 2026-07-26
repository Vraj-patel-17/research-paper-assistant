from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

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
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    paper_id: int
    user_id: int

    class Config:
        from_attributes = True