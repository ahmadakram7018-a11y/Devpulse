from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.user import UserResponse
from typing import Optional

class CreatePost(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostResponse(BaseModel):
    id : int
    title: str
    content: str
    is_published: bool
    created_at: datetime = datetime.now()    
    owner_id: int
    owner: "UserResponse" # this is a forward reference, because the UserResponse class is defined after the PostResponse class. So we need to use a string to refer to it.

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

