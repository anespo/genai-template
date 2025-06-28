# Contributing to GenAI Template

Thank you for your interest in contributing to the GenAI Template! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Git
- Cookiecutter
- API keys for testing (OpenAI, Gemini, AWS)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/genai-template.git
   cd genai-template
   ```

2. **Test the template locally**
   ```bash
   # Install cookiecutter
   pip install cookiecutter
   
   # Generate a test project
   cookiecutter . --no-input
   
   # Test the generated project
   cd genai_multi_provider_template
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## 🛠️ Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Edit template files in `{{cookiecutter.project_slug}}/`
   - Update `cookiecutter.json` if adding new options
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Generate project with your changes
   cookiecutter . --no-input
   
   # Test the generated project
   cd genai_multi_provider_template
   pip install -e .
   
   # Run tests
   pytest
   
   # Test CLI
   genai_multi_provider_template --help
   
   # Test API
   uvicorn genai_multi_provider_template.api.main:app --reload
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**

### Testing Guidelines

#### Template Testing
- Always test the generated project after making changes
- Ensure all cookiecutter variables work correctly
- Test with different configuration options

#### Generated Project Testing
```bash
# Basic functionality
genai_multi_provider_template providers
genai_multi_provider_template generate --provider openai --prompt "test"

# API testing
curl http://localhost:8000/health

# Docker testing
docker build -t test-genai .
docker run --rm test-genai python -c "import genai_multi_provider_template"
```

#### Provider Testing
- Test with at least one working provider (OpenAI recommended for CI)
- Mock providers for unit tests
- Test error handling for unavailable providers

## 📝 Code Style

### Python Code Style
- Follow PEP 8
- Use Black for formatting: `black genai_multi_provider_template/`
- Use isort for imports: `isort genai_multi_provider_template/`
- Use type hints where possible

### Template Structure
- Keep template files organized and well-commented
- Use meaningful variable names in `cookiecutter.json`
- Maintain consistent indentation and formatting

### Documentation
- Update README.md for new features
- Add docstrings to new functions and classes
- Include examples in documentation

## 🧪 Testing

### Running Tests
```bash
# In the generated project directory
pytest                          # Run all tests
pytest tests/unit/             # Run unit tests only
pytest tests/integration/      # Run integration tests only
pytest --cov=genai_multi_provider_template  # Run with coverage
```

### Writing Tests
- Add unit tests for new functionality
- Mock external API calls
- Test error conditions
- Include integration tests for critical paths

### Test Structure
```
tests/
├── unit/
│   ├── test_client.py
│   ├── test_providers.py
│   └── test_models.py
├── integration/
│   ├── test_api.py
│   └── test_cli.py
└── conftest.py
```

## 📋 Types of Contributions

### 🐛 Bug Fixes
- Fix issues in the template generation
- Fix bugs in the generated project code
- Improve error handling and validation

### ✨ New Features
- Add support for new LLM providers
- Enhance CLI functionality
- Improve UI/UX in Streamlit dashboard
- Add new API endpoints

### 📚 Documentation
- Improve README and documentation
- Add examples and tutorials
- Fix typos and clarify instructions

### 🏗️ Infrastructure
- Improve CI/CD pipelines
- Enhance Docker configuration
- Add monitoring and logging features

## 🔧 Adding New LLM Providers

To add a new LLM provider:

1. **Create provider implementation**
   ```python
   # {{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/providers/new_provider.py
   from .base import BaseProvider
   
   class NewProvider(BaseProvider):
       def __init__(self, api_key: str):
           self.api_key = api_key
       
       async def generate(self, prompt: str, **kwargs):
           # Implementation here
           pass
   ```

2. **Update configuration**
   ```python
   # {{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/config.py
   new_provider_api_key: Optional[str] = Field(default=None, alias="NEW_PROVIDER_API_KEY")
   ```

3. **Register in client**
   ```python
   # {{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/client.py
   if settings.new_provider_api_key:
       self.providers[ProviderType.NEW_PROVIDER] = NewProvider()
   ```

4. **Add tests**
   ```python
   # {{cookiecutter.project_slug}}/tests/unit/test_new_provider.py
   ```

5. **Update documentation**

## 🎯 Cookiecutter Variables

When adding new cookiecutter variables:

1. **Add to cookiecutter.json**
   ```json
   {
     "new_option": ["y", "n"],
     "new_setting": "default_value"
   }
   ```

2. **Use in templates**
   ```python
   {% if cookiecutter.new_option == 'y' %}
   # Include this code
   {% endif %}
   ```

3. **Test all combinations**
   ```bash
   cookiecutter . --no-input new_option=y
   cookiecutter . --no-input new_option=n
   ```

## 📊 Performance Guidelines

- Keep generated projects lightweight
- Use async/await for I/O operations
- Implement proper error handling and retries
- Add appropriate logging and monitoring

## 🔒 Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Follow security best practices for web APIs

## 📢 Communication

### Reporting Issues
- Use GitHub Issues for bug reports and feature requests
- Provide detailed reproduction steps
- Include environment information

### Discussions
- Use GitHub Discussions for questions and ideas
- Join community discussions about new features
- Share your use cases and feedback

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

If you have questions about contributing:
- Check existing GitHub Issues and Discussions
- Create a new Discussion for general questions
- Create an Issue for specific bugs or feature requests

Thank you for contributing to GenAI Template! 🚀
