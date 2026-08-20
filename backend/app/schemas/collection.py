from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class CollectionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CollectionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CollectionResponse(BaseModel):
    id: UUID
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)