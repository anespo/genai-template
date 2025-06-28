# 🤖 GenAI Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Cookiecutter](https://img.shields.io/badge/cookiecutter-template-D4AA00.svg?logo=cookiecutter&logoColor=white)](https://github.com/cookiecutter/cookiecutter)

Un template completo e production-ready per progetti di **Generative AI** con supporto multi-provider (AWS Bedrock, OpenAI, Google Gemini).

![GenAI Template Architecture](https://raw.githubusercontent.com/your-username/genai-template/main/docs/architecture.png)

## 🚀 Caratteristiche

### 🔗 **Multi-Provider Support**
- **AWS Bedrock** - Claude, Titan, Jurassic models
- **OpenAI** - GPT-4, GPT-3.5-turbo, e altri
- **Google Gemini** - Gemini Pro, Gemini Pro Vision

### 🏗️ **Architettura Completa**
- **FastAPI** backend con API REST async
- **Streamlit** dashboard interattiva
- **CLI** per automazione e batch processing
- **Docker** per deployment containerizzato

### 🛠️ **Funzionalità Avanzate**
- ✅ Interfaccia unificata per tutti i provider
- ✅ Batch processing asincrono
- ✅ Monitoring e logging strutturato
- ✅ Test completi (unit + integration)
- ✅ Configurazione basata su environment
- ✅ Health checks e metriche
- ✅ Gestione errori robusta

## 📋 Prerequisiti

- Python 3.11+
- [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)
- API keys per i provider che vuoi utilizzare:
  - OpenAI API key
  - Google Gemini API key
  - AWS credentials configurate (per Bedrock)

## 🚀 Quick Start

### 1. Genera il progetto

```bash
# Installa cookiecutter se non ce l'hai
pip install cookiecutter

# Genera il progetto dal template
cookiecutter https://github.com/your-username/genai-template

# Rispondi alle domande del template
```

### 2. Setup dell'ambiente

```bash
# Naviga nella directory del progetto
cd your-project-name

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Configurazione

```bash
# Copia il file di configurazione
cp .env.example .env

# Modifica .env con le tue API keys
nano .env
```

Esempio di configurazione `.env`:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# Google Gemini Configuration
GEMINI_API_KEY=your-gemini-key-here

# AWS Configuration (usa ~/.aws/credentials)
AWS_REGION=us-east-1
AWS_PROFILE=default

# Application Settings
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

### 4. Test rapido

```bash
# Verifica i provider disponibili
python -m your_project.cli providers

# Genera testo con OpenAI
python -m your_project.cli generate \
  --provider openai \
  --prompt "Spiega l'intelligenza artificiale in 100 parole"

# Avvia l'API server
uvicorn your_project.api.main:app --reload

# Avvia la dashboard Streamlit
streamlit run your_project/ui/dashboard.py
```

## 📖 Documentazione Completa

### 🖥️ **Command Line Interface (CLI)**

```bash
# Lista tutti i comandi disponibili
your-project --help

# Visualizza provider e modelli disponibili
your-project providers
your-project models openai

# Generazione testo
your-project generate \
  --provider openai \
  --model gpt-4 \
  --prompt "Your prompt here" \
  --max-tokens 500 \
  --temperature 0.7

# Chat interattiva
your-project chat --provider gemini --system "You are a helpful assistant"

# Batch processing
your-project batch \
  --provider bedrock \
  --input prompts.txt \
  --output results.json \
  --concurrent 5
```

### 🌐 **API REST (FastAPI)**

```bash
# Avvia il server
uvicorn your_project.api.main:app --host 0.0.0.0 --port 8000

# Documentazione interattiva disponibile su:
# http://localhost:8000/docs
```

Esempi di chiamate API:

```bash
# Health check
curl http://localhost:8000/health

# Generazione testo
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Explain quantum computing",
       "provider": "openai",
       "model": "gpt-4",
       "max_tokens": 200
     }'

# Chat completion
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [
         {"role": "user", "content": "Hello!"}
       ],
       "provider": "gemini"
     }'
```

### 🎨 **Dashboard Streamlit**

```bash
# Avvia la dashboard
streamlit run your_project/ui/dashboard.py

# Accedi a http://localhost:8501
```

Funzionalità della dashboard:
- 💬 Chat interattiva con tutti i provider
- 📝 Generazione testi con parametri personalizzabili
- 📊 Batch processing con upload file
- 📈 Analytics e statistiche d'uso
- ⚙️ Configurazione provider in tempo reale

### 🐳 **Docker Deployment**

```bash
# Build dell'immagine
docker build -t your-project .

# Run del container
docker run -p 8000:8000 --env-file .env your-project

# Oppure usa docker-compose per tutti i servizi
docker-compose up
```

Il `docker-compose.yml` include:
- API server (FastAPI)
- Dashboard UI (Streamlit)
- Prometheus (metriche)
- Grafana (monitoring)

## 🧪 Testing

```bash
# Installa dipendenze di sviluppo
pip install -r requirements-dev.txt

# Esegui tutti i test
pytest

# Test con coverage
pytest --cov=your_project --cov-report=html

# Test specifici
pytest tests/unit/
pytest tests/integration/
```

## 🏗️ Architettura del Progetto

```
your-project/
├── 📁 your_project/
│   ├── 📁 providers/          # Implementazioni LLM
│   │   ├── base.py           # Interfaccia base
│   │   ├── openai_provider.py
│   │   ├── bedrock_provider.py
│   │   └── gemini_provider.py
│   ├── 📁 api/               # FastAPI backend
│   │   └── main.py
│   ├── 📁 cli/               # Command line interface
│   │   └── main.py
│   ├── 📁 ui/                # Streamlit dashboard
│   │   └── dashboard.py
│   ├── client.py             # Client unificato
│   ├── config.py             # Configurazione
│   └── models.py             # Modelli Pydantic
├── 📁 tests/                 # Test suite
│   ├── unit/
│   └── integration/
├── 🐳 Dockerfile
├── ⚙️ docker-compose.yml
├── 📋 requirements.txt
└── 📄 README.md
```

## 🔧 Personalizzazione

### Aggiungere un nuovo provider LLM

1. Crea una nuova classe in `providers/`:

```python
from .base import BaseProvider

class MyCustomProvider(BaseProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def generate(self, prompt: str, **kwargs):
        # Implementa la logica del provider
        pass
```

2. Registra il provider in `client.py`
3. Aggiungi la configurazione in `config.py`
4. Aggiorna i test

### Estendere l'API

Aggiungi nuovi endpoint in `api/main.py`:

```python
@app.post("/custom-endpoint")
async def custom_endpoint(request: CustomRequest):
    # Implementa la logica
    pass
```

## 📊 Monitoring e Logging

Il template include monitoring integrato:

- **Structured Logging** con structlog
- **Metriche Prometheus** per API calls, latenza, errori
- **Health Checks** per tutti i provider
- **Dashboard Grafana** (via docker-compose)

## 🤝 Contributing

1. Fork il repository
2. Crea un feature branch (`git checkout -b feature/amazing-feature`)
3. Commit le modifiche (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

## 📄 License

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🆘 Support

- 📖 [Documentazione completa](https://github.com/your-username/genai-template/wiki)
- 🐛 [Segnala un bug](https://github.com/your-username/genai-template/issues)
- 💡 [Richiedi una feature](https://github.com/your-username/genai-template/issues)
- 💬 [Discussioni](https://github.com/your-username/genai-template/discussions)

## 🌟 Use Cases

Questo template è perfetto per:

- 🤖 **Chatbot multi-provider** con fallback automatico
- 📝 **Content generation pipeline** per marketing
- 🔄 **A/B testing** tra diversi modelli LLM
- 📊 **Batch processing** di grandi volumi di testo
- 🎯 **Prototipazione rapida** di applicazioni GenAI
- 🏢 **Applicazioni enterprise** con requisiti di scalabilità

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) per l'eccellente framework web
- [Streamlit](https://streamlit.io/) per la dashboard interattiva
- [Cookiecutter](https://cookiecutter.readthedocs.io/) per il sistema di templating
- La community open source per le librerie utilizzate

---

⭐ **Se questo template ti è utile, lascia una stella su GitHub!** ⭐
