from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

class Gallery(Base):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    category = Column(String(50))
    image_url = Column(String(255))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
