import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse, CompleteStoryNodeResponse, CreateStoryRequest
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


def get_session_id(session_id: Optional[str] = Cookie(None)):
    """Get or create a session ID for the user"""
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """Create a new story job and start processing in the background"""
    # Set the session ID cookie
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    # Create a unique job ID
    job_id = str(uuid.uuid4())
    
    # Create job record
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )
    db.add(job)
    db.commit()
    
    # Start background task
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )
    
    return job


def generate_story_task(job_id: str, theme: str, session_id: str):
    """Background task to generate a story - non-async implementation to avoid blocking the event loop"""
    # Create a new database session for the background task
    db = SessionLocal()
    
    try:
        # Get the job
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        
        if not job:
            return
        
        try:
            job.status = "processing"
            db.commit()
            
            # Generate the story - this is a blocking call but now runs in a separate thread
            story = StoryGenerator.generate_story(db, session_id, theme)
            
            # Update job with story ID and set status to complete
            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            # Update job with error
            job.status = "failed"
            job.error = str(e)
            job.completed_at = datetime.now()
            db.commit()
    finally:
        # Always close the database session
        db.close()


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(
    story_id: int,
    db: Session = Depends(get_db)
):
    """Get a complete story with its entire node tree - accessible to anyone"""
    # Find the story (no session check - anyone can view completed stories)
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Build and return the complete story tree
    complete_story = build_complete_story_tree(db, story)
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    """Build a complete story tree response with all nodes and paths"""
    # Get all nodes for this story
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()
    
    # Create a dictionary of all nodes
    node_dict = {}
    for node in nodes:
        # Create the node response - no need for children since frontend uses options for navigation
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options,
            children={}  # Empty dict - not used by frontend
        )
        node_dict[node.id] = node_response
    
    # Find the root node
    root_node = next((n for n in nodes if n.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story has no root node")
    
    # Create and return the complete story response
    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )


# Import these at the end to avoid circular imports
from db.database import SessionLocal 