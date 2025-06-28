"""Main client for the GenAI application."""

import asyncio
from typing import Optional, List, Dict, Any
from .providers import OpenAIProvider, BedrockProvider, GeminiProvider
from .models import GenerationResponse, ChatMessage, ProviderType
from .config import settings


class GenAIClient:
    """Main client for interacting with multiple LLM providers."""
    
    def __init__(self):
        """Initialize the client with all providers."""
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers based on configuration."""
        # Initialize OpenAI provider
        if settings.openai_api_key:
            try:
                self.providers[ProviderType.OPENAI] = OpenAIProvider()
            except Exception as e:
                print(f"Failed to initialize OpenAI provider: {e}")
        
        # Initialize Bedrock provider
        try:
            self.providers[ProviderType.BEDROCK] = BedrockProvider()
        except Exception as e:
            print(f"Failed to initialize Bedrock provider: {e}")
        
        # Initialize Gemini provider
        if settings.gemini_api_key:
            try:
                self.providers[ProviderType.GEMINI] = GeminiProvider()
            except Exception as e:
                print(f"Failed to initialize Gemini provider: {e}")
    
    async def generate(
        self,
        prompt: str,
        provider: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate text using the specified provider."""
        provider_type = ProviderType(provider)
        
        if provider_type not in self.providers:
            raise ValueError(f"Provider {provider} is not available")
        
        provider_instance = self.providers[provider_type]
        
        return await provider_instance.generate(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            **kwargs
        )
    
    async def chat(
        self,
        messages: List[ChatMessage],
        provider: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate chat completion using the specified provider."""
        provider_type = ProviderType(provider)
        
        if provider_type not in self.providers:
            raise ValueError(f"Provider {provider} is not available")
        
        provider_instance = self.providers[provider_type]
        
        return await provider_instance.chat(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            **kwargs
        )
    
    async def batch_generate(
        self,
        prompts: List[str],
        provider: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        concurrent_requests: int = 5,
        **kwargs
    ) -> List[GenerationResponse]:
        """Generate text for multiple prompts concurrently."""
        semaphore = asyncio.Semaphore(concurrent_requests)
        
        async def generate_single(prompt: str) -> GenerationResponse:
            async with semaphore:
                return await self.generate(
                    prompt=prompt,
                    provider=provider,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
        
        tasks = [generate_single(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all providers."""
        health_status = {}
        
        for provider_type, provider_instance in self.providers.items():
            try:
                health_status[provider_type.value] = await provider_instance.health_check()
            except Exception:
                health_status[provider_type.value] = False
        
        return health_status
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers."""
        return [provider.value for provider in self.providers.keys()]
    
    def get_available_models(self, provider: str) -> List[str]:
        """Get available models for a specific provider."""
        provider_type = ProviderType(provider)
        
        if provider_type not in self.providers:
            raise ValueError(f"Provider {provider} is not available")
        
        return self.providers[provider_type].get_available_models()
    
    def get_provider_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all providers."""
        info = {}
        
        for provider_type, provider_instance in self.providers.items():
            info[provider_type.value] = {
                "available": True,
                "models": provider_instance.get_available_models(),
                "provider_name": provider_instance.provider_name
            }
        
        return info
