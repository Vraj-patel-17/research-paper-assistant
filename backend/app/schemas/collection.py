from pydantic import BaseModel, Field

class CollectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class CollectionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None

class CollectionResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True