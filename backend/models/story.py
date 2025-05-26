from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Story(Base):
    """Story model representing a choose your own adventure story"""
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)  # To track users without authentication
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    nodes = relationship("StoryNode", back_populates="story")


class StoryNode(Base):
    """Node model representing a point in the story with text and choices"""
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String)  # The story text for this node
    is_root = Column(Boolean, default=False)  # Is this the starting node?
    is_ending = Column(Boolean, default=False)  # Is this a terminal node?
    is_winning_ending = Column(Boolean, default=False)  # Is this a winning ending?
    options = Column(JSON, default=list)  # JSON array of options [{"text": str, "node_id": int}]
    
    # Relationships
    story = relationship("Story", back_populates="nodes") 