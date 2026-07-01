from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import field_validator

class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) > 72:
            raise ValueError("Password cannot exceed 72 characters.")
        return password

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # tells SQLAlchemy to read data even if it is not a dict, but an object with attributes, like a SQLAlchemy model instance. This is useful when you want to return a SQLAlchemy model instance as a response from an API endpoint, and you want Pydantic to read the data from the model's attributes instead of expecting a dictionary.
        #in simple,we use it to convert the ORM(SqlAlchemy) model response from DB into the Pydantic, why? Because we can't show/give  all of that data to client because it may contain sensitive dat, thats why we convert DB response (which is ORM model form) into pydantic model to apply rules defined in pydantic.  


        