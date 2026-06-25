from pydantic import BaseModel, EmailStr
from typing import Optional

class VoteCreate(BaseModel):
    post_id: int
    direction : int
