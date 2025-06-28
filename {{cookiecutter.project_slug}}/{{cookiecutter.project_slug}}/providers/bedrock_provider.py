"""AWS Bedrock provider implementation."""

import json
import boto3
from typing import Optional, List, Dict, Any
from botocore.exceptions import ClientError

from .base import BaseProvider
from ..models import GenerationResponse, ChatMessage
from ..config import settings


class BedrockProvider(BaseProvider):
    """AWS Bedrock provider implementation."""
    
    def __init__(self, region: Optional[str] = None, profile: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.region = region or settings.aws_region
        self.profile = profile or settings.aws_profile
        
        # Initialize boto3 session
        session = boto3.Session(profile_name=self.profile)
        self.client = session.client('bedrock-runtime', region_name=self.region)
        
        self.default_model = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate text using AWS Bedrock."""
        model = model or self.default_model
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        top_p = top_p or settings.top_p
        
        try:
            if "anthropic.claude" in model:
                return await self._generate_claude(
                    prompt, model, max_tokens, temperature, top_p, **kwargs
                )
            elif "amazon.titan" in model:
                return await self._generate_titan(
                    prompt, model, max_tokens, temperature, top_p, **kwargs
                )
            elif "ai21.j2" in model:
                return await self._generate_jurassic(
                    prompt, model, max_tokens, temperature, top_p, **kwargs
                )
            else:
                raise ValueError(f"Unsupported Bedrock model: {model}")
                
        except Exception as e:
            raise Exception(f"Bedrock generation failed: {str(e)}")
    
    async def _generate_claude(
        self, prompt: str, model: str, max_tokens: int, 
        temperature: float, top_p: float, **kwargs
    ) -> GenerationResponse:
        """Generate text using Claude models."""
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = self.client.invoke_model(
            modelId=model,
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        
        return GenerationResponse(
            text=result['content'][0]['text'],
            provider=self.provider_name,
            model=model,
            usage={
                "input_tokens": result.get('usage', {}).get('input_tokens'),
                "output_tokens": result.get('usage', {}).get('output_tokens')
            },
            metadata={
                "stop_reason": result.get('stop_reason'),
                "model_id": result.get('model')
            }
        )
    
    async def _generate_titan(
        self, prompt: str, model: str, max_tokens: int,
        temperature: float, top_p: float, **kwargs
    ) -> GenerationResponse:
        """Generate text using Titan models."""
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": temperature,
                "topP": top_p
            }
        }
        
        response = self.client.invoke_model(
            modelId=model,
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        
        return GenerationResponse(
            text=result['results'][0]['outputText'],
            provider=self.provider_name,
            model=model,
            usage={
                "input_tokens": result.get('inputTextTokenCount'),
                "output_tokens": result['results'][0].get('tokenCount')
            },
            metadata={
                "completion_reason": result['results'][0].get('completionReason')
            }
        )
    
    async def _generate_jurassic(
        self, prompt: str, model: str, max_tokens: int,
        temperature: float, top_p: float, **kwargs
    ) -> GenerationResponse:
        """Generate text using Jurassic models."""
        body = {
            "prompt": prompt,
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p
        }
        
        response = self.client.invoke_model(
            modelId=model,
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        
        return GenerationResponse(
            text=result['completions'][0]['data']['text'],
            provider=self.provider_name,
            model=model,
            usage={
                "prompt_tokens": result['prompt']['tokens'],
                "completion_tokens": result['completions'][0]['data']['tokens']
            }
        )
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> GenerationResponse:
        """Generate chat completion using Bedrock."""
        model = model or self.default_model
        
        if "anthropic.claude" in model:
            # Convert messages to Claude format
            claude_messages = []
            for msg in messages:
                claude_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens or settings.max_tokens,
                "temperature": temperature or settings.temperature,
                "top_p": top_p or settings.top_p,
                "messages": claude_messages
            }
            
            response = self.client.invoke_model(
                modelId=model,
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            
            return GenerationResponse(
                text=result['content'][0]['text'],
                provider=self.provider_name,
                model=model,
                usage={
                    "input_tokens": result.get('usage', {}).get('input_tokens'),
                    "output_tokens": result.get('usage', {}).get('output_tokens')
                }
            )
        else:
            # For non-Claude models, convert to single prompt
            prompt = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
            return await self.generate(prompt, model, max_tokens, temperature, top_p, **kwargs)
    
    async def health_check(self) -> bool:
        """Check Bedrock availability."""
        try:
            self.client.list_foundation_models()
            return True
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get available Bedrock models."""
        return [
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-v2:1",
            "amazon.titan-text-express-v1",
            "amazon.titan-text-lite-v1",
            "ai21.j2-ultra-v1",
            "ai21.j2-mid-v1"
        ]
    
    @property
    def provider_name(self) -> str:
        """Get provider name."""
        return "bedrock"
