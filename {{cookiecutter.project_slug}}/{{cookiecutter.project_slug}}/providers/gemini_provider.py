"""Google Gemini provider implementation."""

import asyncio
from typing import Optional, List, Dict, Any
import google.generativeai as genai

from .base import BaseProvider
from ..models import GenerationResponse, ChatMessage
from ..config import settings


class GeminiProvider(BaseProvider):
    """Google Gemini provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or settings.gemini_api_key
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        self.default_model = "gemini-pro"
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate text using Gemini."""
        model_name = model or self.default_model
        temperature = temperature or settings.temperature
        top_p = top_p or settings.top_p
        
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens or settings.max_tokens,
            )
            
            # Initialize model
            gemini_model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            
            # Generate content
            response = await asyncio.to_thread(
                gemini_model.generate_content, prompt
            )
            
            return GenerationResponse(
                text=response.text,
                provider=self.provider_name,
                model=model_name,
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                },
                metadata={
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in response.candidates[0].safety_ratings
                    ] if response.candidates else []
                }
            )
        except Exception as e:
            raise Exception(f"Gemini generation failed: {str(e)}")
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate chat completion using Gemini."""
        model_name = model or self.default_model
        temperature = temperature or settings.temperature
        top_p = top_p or settings.top_p
        
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens or settings.max_tokens,
            )
            
            # Initialize model
            gemini_model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            
            # Convert messages to Gemini chat format
            chat_history = []
            current_prompt = ""
            
            for msg in messages:
                if msg.role == "user":
                    current_prompt = msg.content
                elif msg.role == "assistant":
                    chat_history.append({
                        "parts": [current_prompt],
                        "role": "user"
                    })
                    chat_history.append({
                        "parts": [msg.content],
                        "role": "model"
                    })
                # System messages are handled differently in Gemini
                elif msg.role == "system":
                    # Prepend system message to the first user message
                    if not chat_history:
                        current_prompt = f"{msg.content}\n\n{current_prompt}" if current_prompt else msg.content
            
            # Start chat session
            chat = gemini_model.start_chat(history=chat_history)
            
            # Send the current prompt
            response = await asyncio.to_thread(
                chat.send_message, current_prompt
            )
            
            return GenerationResponse(
                text=response.text,
                provider=self.provider_name,
                model=model_name,
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                },
                metadata={
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in response.candidates[0].safety_ratings
                    ] if response.candidates else []
                }
            )
        except Exception as e:
            raise Exception(f"Gemini chat completion failed: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check Gemini API availability."""
        try:
            models = await asyncio.to_thread(genai.list_models)
            return len(list(models)) > 0
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get available Gemini models."""
        return [
            "gemini-pro",
            "gemini-pro-vision",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
    
    @property
    def provider_name(self) -> str:
        """Get provider name."""
        return "gemini"
