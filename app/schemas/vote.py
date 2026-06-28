from pydantic import BaseModel, field_validator
from datetime import datetime


class CreateVote(BaseModel):
    post_id: int
    direction : int

    
    @field_validator("direction")
    @classmethod
    def direction_must_be_valid(cls, v: int) -> int:
        if v not in (0,1):
            raise ValueError("Direction must be 0 or 1")
        return v
    
   