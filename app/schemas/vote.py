from pydantic import BaseModel
from datetime import datetime
from typing import validator
class CreateVote(BaseModel):
    post_id: int
    direction : int

    @validator("direction")
    def direction_must_be_valid(cls, v):
        if v not in [0, 1]:
            raise ValueError("Direction must be 0 or 1")
        return v
    
   