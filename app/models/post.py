from sqlalchemy import Column, Integer, Boolean, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # ✅

    owner = relationship("User", back_populates="posts")
    