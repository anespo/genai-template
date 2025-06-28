"""Data models for the GenAI application."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class ProviderType(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    BEDROCK = "bedrock"
    GEMINI = "gemini"


class GenerationRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="The input prompt")
    provider: ProviderType = Field(..., description="LLM provider to use")
    model: Optional[str] = Field(None, description="Specific model to use")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, description="Sampling temperature")
    top_p: Optional[float] = Field(None, description="Top-p sampling parameter")
    system_prompt: Optional[str] = Field(None, description="System prompt for chat models")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Explain quantum computing in simple terms",
                "provider": "openai",
                "model": "gpt-4",
                "max_tokens": 500,
                "temperature": 0.7
            }
        }


class GenerationResponse(BaseModel):
    """Response model for text generation."""
    text: str = Field(..., description="Generated text")
    provider: str = Field(..., description="Provider used")
    model: str = Field(..., description="Model used")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Quantum computing is a revolutionary technology...",
                "provider": "openai",
                "model": "gpt-4",
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 150,
                    "total_tokens": 160
                }
            }
        }


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat completion."""
    messages: List[ChatMessage] = Field(..., description="Chat messages")
    provider: ProviderType = Field(..., description="LLM provider to use")
    model: Optional[str] = Field(None, description="Specific model to use")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, description="Sampling temperature")
    top_p: Optional[float] = Field(None, description="Top-p sampling parameter")


class ChatResponse(BaseModel):
    """Response model for chat completion."""
    message: ChatMessage = Field(..., description="Assistant's response message")
    provider: str = Field(..., description="Provider used")
    model: str = Field(..., description="Model used")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class BatchRequest(BaseModel):
    """Request model for batch processing."""
    prompts: List[str] = Field(..., description="List of prompts to process")
    provider: ProviderType = Field(..., description="LLM provider to use")
    model: Optional[str] = Field(None, description="Specific model to use")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, description="Sampling temperature")
    concurrent_requests: int = Field(default=5, description="Number of concurrent requests")


class BatchResponse(BaseModel):
    """Response model for batch processing."""
    results: List[GenerationResponse] = Field(..., description="List of generation results")
    total_processed: int = Field(..., description="Total number of prompts processed")
    success_count: int = Field(..., description="Number of successful generations")
    error_count: int = Field(..., description="Number of failed generations")
    errors: List[str] = Field(default_factory=list, description="List of error messages")


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    providers: Dict[str, bool] = Field(..., description="Provider availability status")
    timestamp: str = Field(..., description="Check timestamp")
