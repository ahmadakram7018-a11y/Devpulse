from sqlalchemy import Base, Column, Integer, String, Boolean , Text
from sqlalchemy.orm import relationship
from app.database import base
from sqlalchemy.sql import func

class Post(base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True, index=True, nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(func.now())
    owner_id = Column(Integer, nullable=False)

    owner = relationship("User", back_populates="posts")