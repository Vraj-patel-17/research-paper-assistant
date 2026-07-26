from pydantic import BaseModel, Field , ConfigDict

class ArxivIngestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(max_length=200, min_length=2)
    max_results: int = Field(default=20, ge=1, le=100)
    start: int = Field(default=0, ge=0)