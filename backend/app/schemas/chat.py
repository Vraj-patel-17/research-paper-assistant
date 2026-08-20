from pydantic import BaseModel,ConfigDict,Field
from typing import Annotated
from uuid import UUID
class ChatRequest(BaseModel):
    model_config=ConfigDict(extra="forbid")
    question: Annotated[str,Field(min_length=3,max_length=1000)]

class SourceReference(BaseModel):
    chunk_index: int
    chunk_id :UUID
    section :str | None=None

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]