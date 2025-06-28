"""OpenAI provider implementation."""

import asyncio
from typing import Optional, List, Dict, Any
import openai
from openai import AsyncOpenAI

from .base import BaseProvider
from ..models import GenerationResponse, ChatMessage
from ..config import settings


class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.default_model = "gpt-3.5-turbo"
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate text using OpenAI."""
        model = model or self.default_model
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        top_p = top_p or settings.top_p
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                **kwargs
            )
            
            return GenerationResponse(
                text=response.choices[0].message.content,
                provider=self.provider_name,
                model=model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id
                }
            )
        except Exception as e:
            raise Exception(f"OpenAI generation failed: {str(e)}")
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate chat completion using OpenAI."""
        model = model or self.default_model
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        top_p = top_p or settings.top_p
        
        # Convert ChatMessage objects to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                **kwargs
            )
            
            return GenerationResponse(
                text=response.choices[0].message.content,
                provider=self.provider_name,
                model=model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id
                }
            )
        except Exception as e:
            raise Exception(f"OpenAI chat completion failed: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check OpenAI API availability."""
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get available OpenAI models."""
        return [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]
    
    @property
    def provider_name(self) -> str:
        """Get provider name."""
        return "openai"
