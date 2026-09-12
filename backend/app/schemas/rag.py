from pydantic import BaseModel


class EmbeddedChunk(BaseModel):
    text: str
    embedding: list[float]
    
class RetrievedChunk(BaseModel):
    text: str
    score: float