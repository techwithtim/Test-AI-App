from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func

from db.database import Base


class StoryJob(Base):
    """Job model for tracking asynchronous story generation"""
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True)  # To track users without authentication
    theme = Column(String)
    status = Column(String)  # "pending", "processing", "completed", "failed"
    story_id = Column(Integer, nullable=True)  # Will be populated when story is created
    error = Column(String, nullable=True)  # Error message if job fails
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True) 