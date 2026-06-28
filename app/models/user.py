from sqlalchemy import Integer, String, Column, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func 

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column (String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    posts = relationship("Post", back_populates="owner")
