"""Test configuration and fixtures."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from test_project.client import GenAIClient
from test_project.providers import OpenAIProvider, BedrockProvider, GeminiProvider
from test_project.models import GenerationResponse


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_openai_provider():
    """Mock OpenAI provider."""
    provider = Mock(spec=OpenAIProvider)
    provider.provider_name = "openai"
    provider.generate = AsyncMock(return_value=GenerationResponse(
        text="Mock OpenAI response",
        provider="openai",
        model="gpt-3.5-turbo",
        usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    ))
    provider.chat = AsyncMock(return_value=GenerationResponse(
        text="Mock OpenAI chat response",
        provider="openai",
        model="gpt-3.5-turbo",
        usage={"prompt_tokens": 15, "completion_tokens": 25, "total_tokens": 40}
    ))
    provider.health_check = AsyncMock(return_value=True)
    provider.get_available_models = Mock(return_value=["gpt-3.5-turbo", "gpt-4"])
    return provider


@pytest.fixture
def mock_bedrock_provider():
    """Mock Bedrock provider."""
    provider = Mock(spec=BedrockProvider)
    provider.provider_name = "bedrock"
    provider.generate = AsyncMock(return_value=GenerationResponse(
        text="Mock Bedrock response",
        provider="bedrock",
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        usage={"input_tokens": 12, "output_tokens": 18}
    ))
    provider.chat = AsyncMock(return_value=GenerationResponse(
        text="Mock Bedrock chat response",
        provider="bedrock",
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        usage={"input_tokens": 16, "output_tokens": 24}
    ))
    provider.health_check = AsyncMock(return_value=True)
    provider.get_available_models = Mock(return_value=["anthropic.claude-3-sonnet-20240229-v1:0"])
    return provider


@pytest.fixture
def mock_gemini_provider():
    """Mock Gemini provider."""
    provider = Mock(spec=GeminiProvider)
    provider.provider_name = "gemini"
    provider.generate = AsyncMock(return_value=GenerationResponse(
        text="Mock Gemini response",
        provider="gemini",
        model="gemini-pro",
        usage={"prompt_tokens": 8, "completion_tokens": 22, "total_tokens": 30}
    ))
    provider.chat = AsyncMock(return_value=GenerationResponse(
        text="Mock Gemini chat response",
        provider="gemini",
        model="gemini-pro",
        usage={"prompt_tokens": 14, "completion_tokens": 26, "total_tokens": 40}
    ))
    provider.health_check = AsyncMock(return_value=True)
    provider.get_available_models = Mock(return_value=["gemini-pro", "gemini-pro-vision"])
    return provider


@pytest.fixture
def mock_client(mock_openai_provider, mock_bedrock_provider, mock_gemini_provider):
    """Mock GenAI client with all providers."""
    client = GenAIClient()
    client.providers = {
        "openai": mock_openai_provider,
        "bedrock": mock_bedrock_provider,
        "gemini": mock_gemini_provider
    }
    return client


@pytest.fixture
def sample_generation_request():
    """Sample generation request data."""
    return {
        "prompt": "Test prompt",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "max_tokens": 100,
        "temperature": 0.7
    }


@pytest.fixture
def sample_chat_messages():
    """Sample chat messages."""
    from test_project.models import ChatMessage
    return [
        ChatMessage(role="user", content="Hello"),
        ChatMessage(role="assistant", content="Hi there!"),
        ChatMessage(role="user", content="How are you?")
    ]
