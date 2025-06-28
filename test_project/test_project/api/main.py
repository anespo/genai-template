"""FastAPI main application."""

from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import structlog

from ..client import GenAIClient
from ..models import (
    GenerationRequest, GenerationResponse, ChatRequest, ChatResponse,
    BatchRequest, BatchResponse, HealthCheck
)
from ..config import settings
from .. import __version__

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Test GenAI Project",
    description="A comprehensive template for Generative AI projects with multiple LLM providers",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GenAI client
client = GenAIClient()


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting GenAI API server", version=__version__)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down GenAI API server")


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    try:
        provider_status = await client.health_check()
        
        return HealthCheck(
            status="healthy",
            version=__version__,
            providers=provider_status,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    """Generate text using the specified provider."""
    try:
        logger.info(
            "Text generation request",
            provider=request.provider,
            model=request.model,
            prompt_length=len(request.prompt)
        )
        
        response = await client.generate(
            prompt=request.prompt,
            provider=request.provider.value,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        logger.info(
            "Text generation completed",
            provider=response.provider,
            model=response.model,
            response_length=len(response.text)
        )
        
        return response
        
    except Exception as e:
        logger.error("Text generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Generate chat completion using the specified provider."""
    try:
        logger.info(
            "Chat completion request",
            provider=request.provider,
            model=request.model,
            message_count=len(request.messages)
        )
        
        response = await client.chat(
            messages=request.messages,
            provider=request.provider.value,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        # Convert to ChatResponse format
        from ..models import ChatMessage
        chat_response = ChatResponse(
            message=ChatMessage(role="assistant", content=response.text),
            provider=response.provider,
            model=response.model,
            usage=response.usage,
            metadata=response.metadata
        )
        
        logger.info(
            "Chat completion completed",
            provider=response.provider,
            model=response.model,
            response_length=len(response.text)
        )
        
        return chat_response
        
    except Exception as e:
        logger.error("Chat completion failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch", response_model=BatchResponse)
async def batch_generate(request: BatchRequest, background_tasks: BackgroundTasks):
    """Process multiple prompts in batch."""
    try:
        logger.info(
            "Batch generation request",
            provider=request.provider,
            model=request.model,
            prompt_count=len(request.prompts),
            concurrent_requests=request.concurrent_requests
        )
        
        results = await client.batch_generate(
            prompts=request.prompts,
            provider=request.provider.value,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            concurrent_requests=request.concurrent_requests
        )
        
        # Process results and separate successful from failed
        successful_results = []
        errors = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append(f"Prompt {i}: {str(result)}")
            else:
                successful_results.append(result)
        
        response = BatchResponse(
            results=successful_results,
            total_processed=len(request.prompts),
            success_count=len(successful_results),
            error_count=len(errors),
            errors=errors
        )
        
        logger.info(
            "Batch generation completed",
            total_processed=response.total_processed,
            success_count=response.success_count,
            error_count=response.error_count
        )
        
        return response
        
    except Exception as e:
        logger.error("Batch generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/providers")
async def get_providers():
    """Get available providers and their information."""
    try:
        return {
            "available_providers": client.get_available_providers(),
            "provider_info": client.get_provider_info()
        }
    except Exception as e:
        logger.error("Failed to get providers", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/providers/{provider}/models")
async def get_provider_models(provider: str):
    """Get available models for a specific provider."""
    try:
        models = client.get_available_models(provider)
        return {"provider": provider, "models": models}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to get provider models", provider=provider, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=True
    )
