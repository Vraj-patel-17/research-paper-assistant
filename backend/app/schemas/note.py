from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    content: str

class NoteUpdate(BaseModel):
    content: str

class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    paper_id: int
    user_id: int

    class Config:
        from_attributes = True