from pydantic import BaseModel, ConfigDict, Field

class AddPaperToCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_id: int = Field(gt=0)