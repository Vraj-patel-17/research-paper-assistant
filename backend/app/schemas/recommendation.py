from pydantic import BaseModel, ConfigDict
from app.schemas.paper import PaperDetailResponse
class RecommendationResponse(BaseModel):
    paper: PaperDetailResponse
    shared_topics: list[str]
    shared_topic_count: int
    reason: str

    model_config = ConfigDict(from_attributes=True)