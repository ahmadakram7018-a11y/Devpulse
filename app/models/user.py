from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy import relationship
from app.database import base
from sqlalchemy.sql import func 

class User(base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column (String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(func.now())

    owner = relationship("Post", back_potulates="owner")
