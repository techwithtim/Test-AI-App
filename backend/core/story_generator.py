from sqlalchemy.orm import Session
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
import os

load_dotenv()


class StoryGenerator:
    """Service for generating complete AI-powered stories with all paths"""
    
    @classmethod
    def _get_llm(cls):
        """Get the LLM client using Choreo-provided environment variables"""
        openai_api_key = os.getenv("CHOREO_OPENAI_2_OPENAI_API_KEY")
        openai_service_url = os.getenv("CHOREO_OPENAI_2_SERVICEURL")
        print("Environment variables:",openai_api_key, openai_service_url)
        if openai_api_key and openai_service_url:
            # Use base_url for OpenAI endpoint override
            return ChatOpenAI(model="gpt-4-turbo", api_key=openai_api_key, base_url=openai_service_url)
        elif openai_api_key:
            return ChatOpenAI(model="gpt-4-turbo", api_key=openai_api_key)
        else:
            return ChatOpenAI(model="gpt-4-turbo")
    
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        """Generate a complete story with all possible paths in a single call"""
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create a new choose-your-own-adventure story with this theme: {theme} and a depth of at least 5"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())
        
        # Generate the entire story in one shot
        raw_response = llm.invoke(prompt.invoke({}))
        
        # Check if response is a string or an object with content attribute
        response_text = raw_response
        if hasattr(raw_response, 'content'):
            response_text = raw_response.content
        
        # Parse the response directly using Pydantic parser
        story_structure = story_parser.parse(response_text)
        
        # Create story in database
        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()  # Get the story ID
        
        # Process the story tree and build it in the database
        root_node_data = story_structure.rootNode
        # If rootNode is a dictionary, parse it into a StoryNodeLLM instance
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        
        db.commit()
        return story_db
    
    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        """Process a node from the story data and add it to the database"""
        # Create the node
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, 'content') else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, 'isEnding') else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, 'isWinningEnding') else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()  # Get the ID
        
        # If not an ending node and has options, process them
        if not node.is_ending and (hasattr(node_data, 'options') and node_data.options):
            options_list = []
            for option_data in node_data.options:
                # Process the child node
                next_node = option_data.nextNode
                # If nextNode is a dictionary, parse it into a StoryNodeLLM instance
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)
                
                child_node = cls._process_story_node(
                    db, 
                    story_id, 
                    next_node,
                    is_root=False
                )
                
                # Add the option to our list
                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })
            
            # Assign the complete options list to ensure SQLAlchemy detects the change
            node.options = options_list
        
        db.flush()
        return node

