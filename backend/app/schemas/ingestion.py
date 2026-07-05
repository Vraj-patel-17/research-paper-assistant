from pydantic import BaseModel, Field

class ArxivIngestionRequest(BaseModel):
    query: str = Field(..., min_length=1)
    max_results: int = Field(default=20, ge=1, le=100)
    start: int = Field(default=0, ge=0)