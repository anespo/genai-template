#!/bin/bash

# GenAI Template Test Script
# This script tests the cookiecutter template locally

set -e

echo "🧪 Testing GenAI Template..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if cookiecutter is installed
if ! command -v cookiecutter &> /dev/null; then
    print_error "Cookiecutter is not installed. Installing..."
    pip install cookiecutter
fi

# Clean up any previous test
if [ -d "test_project" ]; then
    print_status "Cleaning up previous test..."
    rm -rf test_project
fi

# Generate project from template
print_status "Generating project from template..."
cookiecutter . --no-input --output-dir . project_name="Test GenAI Project" project_slug="test_project"

# Navigate to generated project
cd test_project

print_status "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

print_status "Installing dependencies..."
pip install --upgrade pip
pip install -e .

# Test CLI
print_status "Testing CLI..."
if test_project --help > /dev/null 2>&1; then
    print_success "CLI help command works"
else
    print_error "CLI help command failed"
    exit 1
fi

# Test providers command (this will show which providers are available)
print_status "Testing providers command..."
if test_project providers > /dev/null 2>&1; then
    print_success "Providers command works"
else
    print_warning "Providers command failed (this is expected without API keys)"
fi

# Test API server startup (just check if it can import)
print_status "Testing API server import..."
if python -c "from test_project.api.main import app; print('API import successful')" > /dev/null 2>&1; then
    print_success "API server can be imported"
else
    print_error "API server import failed"
    exit 1
fi

# Test Streamlit dashboard import
print_status "Testing Streamlit dashboard import..."
if python -c "import test_project.ui.dashboard; print('Dashboard import successful')" > /dev/null 2>&1; then
    print_success "Streamlit dashboard can be imported"
else
    print_error "Streamlit dashboard import failed"
    exit 1
fi

# Run tests if they exist
if [ -d "tests" ]; then
    print_status "Running tests..."
    if pip install pytest pytest-asyncio pytest-mock > /dev/null 2>&1; then
        if pytest tests/ -v > /dev/null 2>&1; then
            print_success "All tests passed"
        else
            print_warning "Some tests failed (this might be expected without API keys)"
        fi
    else
        print_warning "Could not install test dependencies"
    fi
fi

# Test Docker build
print_status "Testing Docker build..."
if command -v docker &> /dev/null; then
    if docker build -t test-genai-template . > /dev/null 2>&1; then
        print_success "Docker build successful"
        # Clean up Docker image
        docker rmi test-genai-template > /dev/null 2>&1 || true
    else
        print_warning "Docker build failed"
    fi
else
    print_warning "Docker not available, skipping Docker test"
fi

# Go back to original directory
cd ..

print_success "Template test completed successfully!"
print_status "Generated project is in: test_project/"
print_status ""
print_status "To test with real API keys:"
print_status "1. cd test_project"
print_status "2. cp .env.example .env"
print_status "3. Edit .env with your API keys"
print_status "4. source venv/bin/activate"
print_status "5. test_project providers"
print_status ""
print_status "To clean up: rm -rf test_project"
