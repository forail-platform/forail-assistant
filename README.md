# Forge Assistant

AI-powered assistant for the Forge infrastructure automation platform. Uses a local Ollama LLM with RAG (Retrieval-Augmented Generation) to provide contextual help, error analysis, and documentation search.

## Overview

Forge Assistant is an **optional, standalone service** that can be plugged into or removed from any Forge deployment. It runs as a separate container alongside Ollama (LLM) and ChromaDB (vector store).

```
┌──────────────────┐     ┌────────────────┐     ┌─────────────┐
│  Forge Frontend  │────▶│ Forge Assistant │────▶│   Ollama     │
│  (React chat)    │ SSE │ (FastAPI)       │     │ mistral:7b   │
└──────────────────┘     └───────┬─────────┘     └─────────────┘
                                 │
                          ┌──────▼──────┐
                          │  ChromaDB   │
                          │ (vector DB) │
                          └─────────────┘
```

## Features

- **Contextual help** — knows which page the user is on
- **Documentation search** — RAG-powered answers from indexed Forge/Ansible docs
- **Error explanation** — analyze failed job output
- **Streaming responses** — token-by-token display via Server-Sent Events
- **Privacy-first** — all data stays on your server, no cloud APIs

## Quick Start

```bash
# Start all services (Ollama + ChromaDB + Assistant)
docker compose up -d

# Pull LLM models (first time only — takes a few minutes)
docker compose run --rm setup

# Index documentation
curl -X POST http://localhost:8100/api/v1/index

# Test it
curl -X POST http://localhost:8100/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "How do I create a job template?"}'
```

## Integration with Forge

To add the assistant to an existing Forge deployment:

```bash
cd /opt/forge
docker compose -f docker-compose.yml -f path/to/forge-assistant/docker-compose.integration.yml up -d
```

The frontend automatically detects the assistant via health check and shows the chat button.

## Configuration

All settings via environment variables with `FORGE_ASSISTANT_` prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `FORGE_ASSISTANT_OLLAMA_BASE_URL` | `http://ollama:11434` | Ollama API URL |
| `FORGE_ASSISTANT_OLLAMA_MODEL` | `mistral:7b` | LLM model |
| `FORGE_ASSISTANT_OLLAMA_EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `FORGE_ASSISTANT_CHROMA_HOST` | `chromadb` | ChromaDB host |
| `FORGE_ASSISTANT_CHROMA_PORT` | `8000` | ChromaDB port |
| `FORGE_ASSISTANT_RAG_TOP_K` | `5` | Number of docs to retrieve |
| `FORGE_ASSISTANT_LOG_LEVEL` | `INFO` | Logging level |

## Hardware Requirements

| Setup | RAM | GPU | Response Time |
|-------|-----|-----|---------------|
| CPU-only (phi3:mini) | 8 GB | None | 10-20s |
| GPU (mistral:7b) | 16 GB | 8 GB VRAM | 2-5s |
| GPU (llama3.1:8b) | 32 GB | 12 GB VRAM | 1-3s |

## Development

```bash
# Install dependencies
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Lint
ruff check app/ tests/

# Run dev server
uvicorn app.main:app --reload --port 8100
```

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check (Ollama + ChromaDB status) |
| `/api/v1/chat` | POST | Chat with SSE streaming |
| `/api/v1/index` | POST | Trigger document re-indexing |
| `/api/v1/docs` | GET | OpenAPI documentation |

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Configuration](docs/configuration.md)
- [Deployment](docs/deployment.md)

## License

Part of the [Forge Platform](https://github.com/forgeplatform).
