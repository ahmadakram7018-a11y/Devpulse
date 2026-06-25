from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.schemas.user import UserResponse

class PostCreate(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_published: Optional[bool]

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime
    owner_id: int
    owner : UserResponse

    class Config:
        from_attributes = True

