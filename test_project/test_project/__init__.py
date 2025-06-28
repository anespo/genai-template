"""
Test GenAI Project
A comprehensive template for Generative AI projects with multiple LLM providers
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import GenAIClient
from .config import Settings
from .providers import BedrockProvider, OpenAIProvider, GeminiProvider

__all__ = [
    "GenAIClient",
    "Settings", 
    "BedrockProvider",
    "OpenAIProvider", 
    "GeminiProvider"
]
