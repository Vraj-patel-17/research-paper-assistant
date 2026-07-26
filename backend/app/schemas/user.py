from pydantic import BaseModel , ConfigDict ,EmailStr , Field
from typing import Annotated
class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username : Annotated[str,Field(min_length=3,max_length=20)]
    email : EmailStr
    password : Annotated[str,Field(min_length=8,max_length=120)]
class UserResponse(BaseModel):
    id : int
    username : str
    email : EmailStr
    class Config:
        from_attributes=True
class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password : Annotated[str,Field(min_length=8,max_length=120)]