from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # tells SQLAlchemy to read data even if it is not a dict, but an object with attributes, like a SQLAlchemy model instance. This is useful when you want to return a SQLAlchemy model instance as a response from an API endpoint, and you want Pydantic to read the data from the model's attributes instead of expecting a dictionary.