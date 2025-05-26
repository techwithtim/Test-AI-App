from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings. Load environment variables from .env file
    """
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # CORS
    ALLOWED_ORIGINS: str = ""
    
    # KEYS
    OPENAI_API_KEY: str
    
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        """Parse comma-separated list of allowed origins"""
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings() 