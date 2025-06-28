"""Unit tests for the GenAI client."""

import pytest
from unittest.mock import Mock, AsyncMock

from test_project.client import GenAIClient
from test_project.models import ChatMessage


class TestGenAIClient:
    """Test cases for GenAIClient."""
    
    @pytest.mark.asyncio
    async def test_generate_success(self, mock_client, sample_generation_request):
        """Test successful text generation."""
        response = await mock_client.generate(**sample_generation_request)
        
        assert response.text == "Mock OpenAI response"
        assert response.provider == "openai"
        assert response.model == "gpt-3.5-turbo"
        assert response.usage["total_tokens"] == 30
    
    @pytest.mark.asyncio
    async def test_generate_invalid_provider(self, mock_client):
        """Test generation with invalid provider."""
        with pytest.raises(ValueError, match="Provider invalid is not available"):
            await mock_client.generate(
                prompt="Test",
                provider="invalid"
            )
    
    @pytest.mark.asyncio
    async def test_chat_success(self, mock_client, sample_chat_messages):
        """Test successful chat completion."""
        response = await mock_client.chat(
            messages=sample_chat_messages,
            provider="openai"
        )
        
        assert response.text == "Mock OpenAI chat response"
        assert response.provider == "openai"
        assert response.usage["total_tokens"] == 40
    
    @pytest.mark.asyncio
    async def test_batch_generate_success(self, mock_client):
        """Test successful batch generation."""
        prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
        
        results = await mock_client.batch_generate(
            prompts=prompts,
            provider="openai",
            concurrent_requests=2
        )
        
        assert len(results) == 3
        for result in results:
            assert result.text == "Mock OpenAI response"
            assert result.provider == "openai"
    
    @pytest.mark.asyncio
    async def test_health_check(self, mock_client):
        """Test provider health check."""
        health_status = await mock_client.health_check()
        
        assert health_status["openai"] is True
        assert health_status["bedrock"] is True
        assert health_status["gemini"] is True
    
    def test_get_available_providers(self, mock_client):
        """Test getting available providers."""
        providers = mock_client.get_available_providers()
        
        assert "openai" in providers
        assert "bedrock" in providers
        assert "gemini" in providers
    
    def test_get_available_models(self, mock_client):
        """Test getting available models for a provider."""
        models = mock_client.get_available_models("openai")
        
        assert "gpt-3.5-turbo" in models
        assert "gpt-4" in models
    
    def test_get_available_models_invalid_provider(self, mock_client):
        """Test getting models for invalid provider."""
        with pytest.raises(ValueError, match="Provider invalid is not available"):
            mock_client.get_available_models("invalid")
    
    def test_get_provider_info(self, mock_client):
        """Test getting provider information."""
        info = mock_client.get_provider_info()
        
        assert "openai" in info
        assert "bedrock" in info
        assert "gemini" in info
        
        assert info["openai"]["available"] is True
        assert "gpt-3.5-turbo" in info["openai"]["models"]
