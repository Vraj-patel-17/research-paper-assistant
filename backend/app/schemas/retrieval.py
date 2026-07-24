from dataclasses import dataclass
from pydantic import BaseModel
@dataclass
class RetrievedChunk:
    chunk_id: int
    chunk_index: int
    content: str
    section: str | None
    score: float

class RetrievedChunkResponse(BaseModel):
    chunk_id: int
    chunk_index: int
    section: str | None
    score: float
    content: str


class RetrievalDebugResponse(BaseModel):
    chunks: list[RetrievedChunkResponse]