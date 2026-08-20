from pydantic import BaseModel , ConfigDict ,EmailStr , Field
from typing import Annotated
from uuid import UUID
class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username : Annotated[str,Field(min_length=3,max_length=20)]
    email : EmailStr
    password : Annotated[str,Field(min_length=8,max_length=120)]
class UserResponse(BaseModel):
    id : UUID
    username : str
    email : EmailStr
    model_config = ConfigDict(from_attributes=True)
class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password : Annotated[str,Field(min_length=8,max_length=120)]