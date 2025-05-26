import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


def get_session_id(session_id: Optional[str] = Cookie(None)):
    """Get or create a session ID for the user"""
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@router.get("/{job_id}", response_model=StoryJobResponse)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Get the status of a story generation job - accessible to anyone"""
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job 