# Examples

This document provides practical examples of using the GenAI Template.

## 🚀 Quick Start Examples

### Basic Text Generation

```bash
# Generate with OpenAI
genai-project generate \
  --provider openai \
  --prompt "Write a haiku about programming" \
  --max-tokens 50

# Generate with Gemini
genai-project generate \
  --provider gemini \
  --prompt "Explain quantum computing in simple terms" \
  --temperature 0.3

# Generate with Bedrock (Claude)
genai-project generate \
  --provider bedrock \
  --model "anthropic.claude-3-sonnet-20240229-v1:0" \
  --prompt "Create a product description for a smart watch"
```

### Interactive Chat

```bash
# Start chat with system prompt
genai-project chat \
  --provider openai \
  --system "You are a helpful Python programming assistant"

# Chat with Gemini
genai-project chat \
  --provider gemini \
  --system "You are a creative writing coach"
```

### Batch Processing

```bash
# Create input file
cat > prompts.txt << EOF
Write a summary of machine learning
Explain neural networks
What is deep learning?
How does NLP work?
EOF

# Process batch
genai-project batch \
  --provider openai \
  --input prompts.txt \
  --output results.json \
  --concurrent 3 \
  --max-tokens 200
```

## 🌐 API Examples

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "providers": {
    "openai": true,
    "bedrock": false,
    "gemini": true
  },
  "timestamp": "2025-06-28T21:00:00.000Z"
}
```

### Text Generation

```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Create a marketing slogan for an AI startup",
       "provider": "openai",
       "model": "gpt-4",
       "max_tokens": 100,
       "temperature": 0.8
     }'
```

Response:
```json
{
  "text": "Empowering Tomorrow, Today - Where AI Meets Innovation",
  "provider": "openai",
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "total_tokens": 20
  },
  "metadata": {
    "finish_reason": "stop",
    "response_id": "chatcmpl-..."
  }
}
```

### Chat Completion

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [
         {"role": "system", "content": "You are a helpful assistant"},
         {"role": "user", "content": "What is the capital of France?"},
         {"role": "assistant", "content": "The capital of France is Paris."},
         {"role": "user", "content": "What is its population?"}
       ],
       "provider": "openai",
       "max_tokens": 150
     }'
```

### Batch Processing

```bash
curl -X POST "http://localhost:8000/batch" \
     -H "Content-Type: application/json" \
     -d '{
       "prompts": [
         "Explain photosynthesis",
         "What is gravity?",
         "How do computers work?"
       ],
       "provider": "gemini",
       "max_tokens": 100,
       "concurrent_requests": 2
     }'
```

## 🐍 Python SDK Examples

### Basic Usage

```python
import asyncio
from your_project import GenAIClient

async def main():
    client = GenAIClient()
    
    # Simple generation
    response = await client.generate(
        prompt="Write a Python function to calculate fibonacci",
        provider="openai",
        model="gpt-4",
        max_tokens=200
    )
    
    print(response.text)
    print(f"Tokens used: {response.usage['total_tokens']}")

asyncio.run(main())
```

### Chat Conversation

```python
import asyncio
from your_project import GenAIClient
from your_project.models import ChatMessage

async def chat_example():
    client = GenAIClient()
    
    messages = [
        ChatMessage(role="system", content="You are a code reviewer"),
        ChatMessage(role="user", content="Review this Python code: def add(a, b): return a + b")
    ]
    
    response = await client.chat(
        messages=messages,
        provider="openai",
        temperature=0.3
    )
    
    print(f"Review: {response.text}")

asyncio.run(chat_example())
```

### Batch Processing

```python
import asyncio
from your_project import GenAIClient

async def batch_example():
    client = GenAIClient()
    
    prompts = [
        "Explain machine learning",
        "What is artificial intelligence?",
        "How does deep learning work?",
        "What are neural networks?"
    ]
    
    results = await client.batch_generate(
        prompts=prompts,
        provider="gemini",
        max_tokens=150,
        concurrent_requests=2
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Error for prompt {i}: {result}")
        else:
            print(f"Result {i}: {result.text[:100]}...")

asyncio.run(batch_example())
```

### Provider Comparison

```python
import asyncio
from your_project import GenAIClient

async def compare_providers():
    client = GenAIClient()
    prompt = "Explain the concept of recursion in programming"
    
    providers = ["openai", "gemini"]
    results = {}
    
    for provider in providers:
        try:
            response = await client.generate(
                prompt=prompt,
                provider=provider,
                max_tokens=200,
                temperature=0.7
            )
            results[provider] = {
                "text": response.text,
                "tokens": response.usage.get("total_tokens", 0) if response.usage else 0
            }
        except Exception as e:
            results[provider] = {"error": str(e)}
    
    for provider, result in results.items():
        print(f"\n--- {provider.upper()} ---")
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Response: {result['text'][:200]}...")
            print(f"Tokens: {result['tokens']}")

asyncio.run(compare_providers())
```

## 🎨 Streamlit Dashboard Examples

### Custom Provider Configuration

```python
import streamlit as st
from your_project import GenAIClient

# Custom sidebar configuration
with st.sidebar:
    st.header("Custom Settings")
    
    # Provider selection with custom options
    provider = st.selectbox(
        "Select Provider",
        ["openai", "gemini", "bedrock"],
        help="Choose your preferred LLM provider"
    )
    
    # Model selection based on provider
    if provider == "openai":
        model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"])
    elif provider == "gemini":
        model = st.selectbox("Model", ["gemini-pro", "gemini-pro-vision"])
    else:
        model = st.selectbox("Model", ["anthropic.claude-3-sonnet-20240229-v1:0"])
    
    # Advanced parameters
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
    max_tokens = st.slider("Max Tokens", 50, 2000, 500)
    
    # Custom system prompt
    system_prompt = st.text_area(
        "System Prompt",
        "You are a helpful AI assistant.",
        help="Set the behavior and context for the AI"
    )
```

### Batch Processing with File Upload

```python
import streamlit as st
import pandas as pd
from your_project import GenAIClient

st.header("Batch Processing")

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV with prompts",
    type=['csv', 'txt'],
    help="CSV should have a 'prompt' column, or TXT with one prompt per line"
)

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        prompts = df['prompt'].tolist()
    else:
        content = uploaded_file.read().decode('utf-8')
        prompts = [line.strip() for line in content.split('\n') if line.strip()]
    
    st.write(f"Found {len(prompts)} prompts")
    
    if st.button("Process Batch"):
        client = GenAIClient()
        
        progress_bar = st.progress(0)
        results = []
        
        for i, prompt in enumerate(prompts):
            try:
                response = await client.generate(
                    prompt=prompt,
                    provider="openai",
                    max_tokens=200
                )
                results.append({
                    "prompt": prompt,
                    "response": response.text,
                    "tokens": response.usage.get("total_tokens", 0)
                })
            except Exception as e:
                results.append({
                    "prompt": prompt,
                    "response": f"Error: {str(e)}",
                    "tokens": 0
                })
            
            progress_bar.progress((i + 1) / len(prompts))
        
        # Display results
        results_df = pd.DataFrame(results)
        st.dataframe(results_df)
        
        # Download results
        csv = results_df.to_csv(index=False)
        st.download_button(
            "Download Results",
            csv,
            "batch_results.csv",
            "text/csv"
        )
```

## 🐳 Docker Examples

### Basic Docker Run

```bash
# Build the image
docker build -t my-genai-app .

# Run with environment variables
docker run -d \
  --name genai-app \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e GEMINI_API_KEY=your_key_here \
  my-genai-app
```

### Docker Compose with Monitoring

```yaml
version: '3.8'

services:
  genai-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ~/.aws:/home/genai/.aws:ro
    depends_on:
      - prometheus
      - grafana

  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    command: streamlit run your_project/ui/dashboard.py --server.port 8501 --server.address 0.0.0.0

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## 🧪 Testing Examples

### Unit Test Example

```python
import pytest
from unittest.mock import AsyncMock
from your_project.client import GenAIClient
from your_project.models import GenerationResponse

@pytest.mark.asyncio
async def test_generate_success():
    client = GenAIClient()
    
    # Mock the provider
    mock_response = GenerationResponse(
        text="Test response",
        provider="openai",
        model="gpt-3.5-turbo",
        usage={"total_tokens": 10}
    )
    
    client.providers["openai"].generate = AsyncMock(return_value=mock_response)
    
    response = await client.generate(
        prompt="Test prompt",
        provider="openai"
    )
    
    assert response.text == "Test response"
    assert response.provider == "openai"
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient
from your_project.api.main import app

def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "providers" in data

def test_generate_endpoint():
    client = TestClient(app)
    
    request_data = {
        "prompt": "Test prompt",
        "provider": "openai",
        "max_tokens": 50
    }
    
    response = client.post("/generate", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["provider"] == "openai"
```

## 🔧 Configuration Examples

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-your-openai-key
GEMINI_API_KEY=your-gemini-key
AWS_REGION=us-east-1
AWS_PROFILE=default

# Application settings
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
TOP_P=0.9

# API settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Custom Configuration

```python
from your_project.config import Settings

# Custom settings
settings = Settings(
    openai_api_key="your-key",
    max_tokens=2000,
    temperature=0.5,
    log_level="DEBUG"
)

# Use in client
from your_project.client import GenAIClient
client = GenAIClient(settings=settings)
```

These examples should help you get started with the GenAI Template and explore its various capabilities!
