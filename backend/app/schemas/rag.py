from pydantic import BaseModel,Field


class EmbeddedChunk(BaseModel):
    text: str
    embedding: list[float]
    page: int | None = None


class RetrievedChunk(BaseModel):
    text: str
    score: float
    page: int | None = None


class AskQuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)


class AskQuestionResponse(BaseModel):
    answer: str
    paper_id: str