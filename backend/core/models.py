from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    """Represents a single option in a story node with its outcome for LLM interaction"""
    text: str = Field(description="The text of the option shown to the user")
    nextNode: Dict[str, Any] = Field(description="The next node content and its options")


class StoryNodeLLM(BaseModel):
    """Represents a node in the story for LLM interaction"""
    content: str = Field(description="The main content of this story node")
    isEnding: bool = Field(default=False, description="Whether this node is an ending node")
    isWinningEnding: bool = Field(default=False, description="Whether this node is a winning ending")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="Options for this node")


class StoryLLMResponse(BaseModel):
    """Represents the full story structure returned by the LLM"""
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story with all its branches")
