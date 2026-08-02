from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import hash_password, create_access_token, verify_access_token, verify_password
from app.models.user import User
from app.schemas.user import CreateUser, UserResponse , UserLogin
from app.utils.logger import setup_logger


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

logger = setup_logger(__name__)

@router.post("/login")
def login(credential : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email==credential.username).first()

    if not user:
        logger.warning(f"Login attempt with non-existent email: {credential.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "invalid credentials"
        )
    
    if not verify_password(credential.password, user.password):
        logger.warning(f"Failed login attempt for user: {credential.username}")
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials")
    

    logger.info(f"User {user.id} logged in successfully") 
    token = create_access_token(data={"user_id": user.id})

       
    return {
            "access_token": token,
            "token_type": "bearer"
        }

    
