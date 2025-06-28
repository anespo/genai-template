# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## 🚀 Features

- **Multi-Provider Support**: AWS Bedrock, OpenAI, and Google Gemini
- **Unified Interface**: Single API for all LLM providers
- **Production Ready**: FastAPI backend with async support
- **Interactive UI**: Streamlit dashboard for testing and demos
- **Docker Support**: Containerized deployment
- **Comprehensive Testing**: Unit and integration tests
- **Configuration Management**: Environment-based settings
- **Logging & Monitoring**: Structured logging and metrics

## 📋 Prerequisites

- Python {{ cookiecutter.python_version }}+
- AWS CLI configured (for Bedrock)
- API keys for OpenAI and Gemini

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd {{ cookiecutter.project_slug }}
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# AWS Configuration (uses ~/.aws/credentials by default)
AWS_REGION=us-east-1
AWS_PROFILE=default

# Application Settings
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

## 🚀 Usage

### Command Line Interface

```bash
# Basic text generation
python -m {{ cookiecutter.project_slug }}.cli generate --provider openai --prompt "Hello, world!"

# Chat completion
python -m {{ cookiecutter.project_slug }}.cli chat --provider bedrock --model claude-3-sonnet

# Batch processing
python -m {{ cookiecutter.project_slug }}.cli batch --input prompts.txt --output results.json
```

### Python API

```python
from {{ cookiecutter.project_slug }} import GenAIClient

# Initialize client
client = GenAIClient()

# Generate text with different providers
response_openai = client.generate(
    prompt="Explain quantum computing",
    provider="openai",
    model="gpt-4"
)

response_bedrock = client.generate(
    prompt="Explain quantum computing",
    provider="bedrock",
    model="anthropic.claude-3-sonnet-20240229-v1:0"
)

response_gemini = client.generate(
    prompt="Explain quantum computing",
    provider="gemini",
    model="gemini-pro"
)
```

### FastAPI Server

```bash
# Start the API server
uvicorn {{ cookiecutter.project_slug }}.api.main:app --reload

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Streamlit UI

```bash
# Start the Streamlit dashboard
streamlit run {{ cookiecutter.project_slug }}/ui/dashboard.py

# Dashboard will be available at http://localhost:8501
```

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t {{ cookiecutter.project_slug }} .

# Run the container
docker run -p 8000:8000 --env-file .env {{ cookiecutter.project_slug }}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{ cookiecutter.project_slug }}

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

## 📊 Monitoring

The application includes built-in monitoring and logging:

- **Metrics**: Request counts, latency, error rates
- **Logging**: Structured JSON logs with correlation IDs
- **Health Checks**: `/health` endpoint for monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the {{ cookiecutter.license }} License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact: {{ cookiecutter.author_email }}

## 🔗 Links

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
