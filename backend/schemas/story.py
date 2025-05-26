from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


class StoryOptionSchema(BaseModel):
    """Schema for a story option in API requests/responses"""
    text: str
    node_id: Optional[int] = None


class StoryNodeBase(BaseModel):
    """Base schema for story node data"""
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class CompleteStoryNodeResponse(StoryNodeBase):
    """Node with its complete subtree for full story response"""
    id: int
    children: Dict[int, 'CompleteStoryNodeResponse'] = {}
    options: List[StoryOptionSchema] = []

    class Config:
        from_attributes = True


class StoryBase(BaseModel):
    """Base schema for story data"""
    title: str
    session_id: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStoryRequest(BaseModel):
    """Request body for creating a new story"""
    theme: str


class CompleteStoryResponse(StoryBase):
    """Complete story with full node tree response"""
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attributes = True