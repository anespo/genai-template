"""Base provider interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ..models import GenerationResponse, ChatMessage


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, **kwargs):
        """Initialize the provider with configuration."""
        self.config = kwargs
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate text from a prompt."""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[ChatMessage],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate chat completion."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is available."""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models for this provider."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the provider name."""
        pass
