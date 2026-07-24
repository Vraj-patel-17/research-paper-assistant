from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class SourceReference(BaseModel):
    chunk_index: int
    chunk_id :int
    section :str | None=None

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]