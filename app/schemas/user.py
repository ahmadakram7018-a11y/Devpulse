from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True