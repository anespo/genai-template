"""Configuration management for the GenAI application."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    
    # Gemini Configuration  
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")
    
    # AWS Configuration
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    aws_profile: str = Field(default="default", alias="AWS_PROFILE")
    
    # Generation Settings
    max_tokens: int = Field(default=1000, alias="MAX_TOKENS")
    temperature: float = Field(default=0.7, alias="TEMPERATURE")
    top_p: float = Field(default=0.9, alias="TOP_P")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # API Settings
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_workers: int = Field(default=1, alias="API_WORKERS")
    
    # UI Settings
    streamlit_port: int = Field(default=8501, alias="STREAMLIT_PORT")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, alias="METRICS_PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
