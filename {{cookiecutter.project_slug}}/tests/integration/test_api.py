"""Integration tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from {{ cookiecutter.project_slug }}.api.main import app


@pytest.fixture
def client():
    """Test client for FastAPI app."""
    return TestClient(app)


class TestAPI:
    """Test cases for the FastAPI application."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        with patch('{{ cookiecutter.project_slug }}.api.main.client') as mock_client:
            mock_client.health_check.return_value = {
                "openai": True,
                "bedrock": True,
                "gemini": True
            }
            
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "providers" in data
            assert "timestamp" in data
    
    def test_get_providers(self, client):
        """Test get providers endpoint."""
        with patch('{{ cookiecutter.project_slug }}.api.main.client') as mock_client:
            mock_client.get_available_providers.return_value = ["openai", "bedrock", "gemini"]
            mock_client.get_provider_info.return_value = {
                "openai": {"available": True, "models": ["gpt-3.5-turbo"]}
            }
            
            response = client.get("/providers")
            
            assert response.status_code == 200
            data = response.json()
            assert "available_providers" in data
            assert "provider_info" in data
    
    def test_get_provider_models(self, client):
        """Test get provider models endpoint."""
        with patch('{{ cookiecutter.project_slug }}.api.main.client') as mock_client:
            mock_client.get_available_models.return_value = ["gpt-3.5-turbo", "gpt-4"]
            
            response = client.get("/providers/openai/models")
            
            assert response.status_code == 200
            data = response.json()
            assert data["provider"] == "openai"
            assert "models" in data
    
    def test_get_provider_models_invalid(self, client):
        """Test get models for invalid provider."""
        with patch('{{ cookiecutter.project_slug }}.api.main.client') as mock_client:
            mock_client.get_available_models.side_effect = ValueError("Provider invalid is not available")
            
            response = client.get("/providers/invalid/models")
            
            assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_generate_text(self, client):
        """Test text generation endpoint."""
        with patch('{{ cookiecutter.project_slug }}.api.main.client') as mock_client:
            from {{ cookiecutter.project_slug }}.models import GenerationResponse
            
            mock_response = GenerationResponse(
                text="Generated text",
                provider="openai",
                model="gpt-3.5-turbo",
                usage={"total_tokens": 30}
            )
            mock_client.generate.return_value = mock_response
            
            request_data = {
                "prompt": "Test prompt",
                "provider": "openai",
                "model": "gpt-3.5-turbo"
            }
            
            response = client.post("/generate", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["text"] == "Generated text"
            assert data["provider"] == "openai"
    
    @pytest.mark.asyncio
    async def test_chat_completion(self, client):
        """Test chat completion endpoint."""
        with patch('{{ cookiecutter.project_slug }}.api.main.client') as mock_client:
            from {{ cookiecutter.project_slug }}.models import GenerationResponse
            
            mock_response = GenerationResponse(
                text="Chat response",
                provider="openai",
                model="gpt-3.5-turbo",
                usage={"total_tokens": 40}
            )
            mock_client.chat.return_value = mock_response
            
            request_data = {
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "provider": "openai",
                "model": "gpt-3.5-turbo"
            }
            
            response = client.post("/chat", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"]["content"] == "Chat response"
            assert data["provider"] == "openai"
