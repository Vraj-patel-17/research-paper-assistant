from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AddPaperToCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_id: UUID