from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class StoryJobBase(BaseModel):
    """Base schema for story job data"""
    theme: str


class StoryJobResponse(BaseModel):
    """Response schema for a story generation job"""
    job_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    story_id: Optional[int] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True


class StoryJobCreate(StoryJobBase):
    """Request schema for creating a new story job"""
    pass 