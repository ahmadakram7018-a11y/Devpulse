from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import hash_password
from app.models.user import User
from app.schemas.user import CreateUser, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/",status_code=status.HTTP_201_CREATED ,response_model=UserResponse)
def register_user(user: CreateUser, db : Session= Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    
    new_user = User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
                  
        
