# Deployment Guide

This guide covers various deployment options for projects generated from the GenAI Template.

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Virtual environment tool (venv, conda, etc.)
- API keys for your chosen providers

### Setup
```bash
# Generate project
cookiecutter https://github.com/your-username/genai-template

# Navigate to project
cd your-project-name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Test the setup
python -m your_project.cli providers
```

## 🐳 Docker Deployment

### Single Container
```bash
# Build image
docker build -t your-project .

# Run container
docker run -d \
  --name your-project \
  -p 8000:8000 \
  --env-file .env \
  your-project
```

### Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# Services available:
# - API: http://localhost:8000
# - UI: http://localhost:8501
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

## ☁️ Cloud Deployment

### AWS Deployment

#### AWS ECS (Fargate)
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

docker build -t your-project .
docker tag your-project:latest your-account.dkr.ecr.us-east-1.amazonaws.com/your-project:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/your-project:latest

# Deploy with ECS task definition
```

#### AWS Lambda (Serverless)
```python
# Use AWS Lambda Web Adapter
# Add to Dockerfile:
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.7.0 /lambda-adapter /opt/extensions/lambda-adapter
ENV AWS_LAMBDA_EXEC_WRAPPER=/opt/extensions/lambda-adapter
```

### Google Cloud Platform

#### Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project-id/genai-app
gcloud run deploy --image gcr.io/your-project-id/genai-app --platform managed
```

#### GKE (Kubernetes)
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: genai-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: genai-app
  template:
    metadata:
      labels:
        app: genai-app
    spec:
      containers:
      - name: genai-app
        image: gcr.io/your-project-id/genai-app
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
```

### Azure

#### Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name genai-app \
  --image your-registry/genai-app \
  --cpu 1 \
  --memory 2 \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your-key
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Production .env
OPENAI_API_KEY=your-production-key
GEMINI_API_KEY=your-production-key
AWS_REGION=us-east-1

# Production settings
LOG_LEVEL=INFO
API_WORKERS=4
ENABLE_METRICS=true

# Security
CORS_ORIGINS=["https://yourdomain.com"]
API_KEY_REQUIRED=true
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ui {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### SSL/TLS with Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring & Observability

### Prometheus Metrics
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'genai-app'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "GenAI App Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      }
    ]
  }
}
```

### Logging
```python
# Structured logging configuration
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

## 🔒 Security Best Practices

### API Security
```python
# Add API key authentication
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_api_key(token: str = Security(security)):
    if token.credentials != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return token
```

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/generate")
@limiter.limit("10/minute")
async def generate_text(request: Request, ...):
    # Your endpoint logic
    pass
```

### Input Validation
```python
from pydantic import validator

class GenerationRequest(BaseModel):
    prompt: str
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if len(v) > 10000:
            raise ValueError('Prompt too long')
        return v
```

## 📈 Scaling Strategies

### Horizontal Scaling
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: genai-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: genai-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Balancing
```python
# Multiple provider instances
providers = {
    "openai_1": OpenAIProvider(api_key=key1),
    "openai_2": OpenAIProvider(api_key=key2),
    "gemini_1": GeminiProvider(api_key=key3),
}

# Round-robin or weighted selection
async def get_provider(provider_type: str):
    available = [p for p in providers if p.startswith(provider_type)]
    return random.choice(available)
```

### Caching
```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(expiry=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiry, json.dumps(result))
            return result
        return wrapper
    return decorator
```

## 🚨 Troubleshooting

### Common Issues

#### API Key Issues
```bash
# Check environment variables
env | grep API_KEY

# Test API key validity
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

#### Memory Issues
```bash
# Monitor memory usage
docker stats

# Increase memory limits
docker run -m 2g your-image
```

#### Network Issues
```bash
# Check connectivity
curl -I https://api.openai.com
curl -I https://generativelanguage.googleapis.com

# Check DNS resolution
nslookup api.openai.com
```

### Health Checks
```python
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database(),
        "providers": await check_providers(),
        "memory": check_memory_usage(),
        "disk": check_disk_space()
    }
    
    status = "healthy" if all(checks.values()) else "unhealthy"
    return {"status": status, "checks": checks}
```

### Backup & Recovery
```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz .env docker-compose.yml

# Database backup (if using)
pg_dump your_db > backup.sql

# Restore
tar -xzf backup-20250628.tar.gz
```

This deployment guide should help you get your GenAI application running in various environments, from local development to production cloud deployments.
