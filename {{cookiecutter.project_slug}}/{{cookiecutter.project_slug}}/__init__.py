"""
{{ cookiecutter.project_name }}
{{ cookiecutter.description }}
"""

__version__ = "{{ cookiecutter.version }}"
__author__ = "{{ cookiecutter.author_name }}"
__email__ = "{{ cookiecutter.author_email }}"

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
