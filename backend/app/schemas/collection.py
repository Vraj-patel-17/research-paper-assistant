from pydantic import BaseModel, Field, ConfigDict

class CollectionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field( min_length=1, max_length=100)
    description: str | None = Field(default=None,max_length=500)

class CollectionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None,max_length=500)

class CollectionResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True