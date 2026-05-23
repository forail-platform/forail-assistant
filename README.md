# Forge Assistant

> ⚠️ **Status: Under active development — not yet production-ready.**
> The AI assistant is shipped as a **preview** to gather early feedback. APIs, models, default prompts, and capabilities may change between releases. Do not depend on it for critical workflows.

AI-powered assistant for the Forge infrastructure automation platform. Uses a local Ollama LLM with RAG (Retrieval-Augmented Generation) to provide contextual help, error analysis, and documentation search.

## Overview

Forge Assistant is an **optional, standalone service** that can be plugged into or removed from any Forge deployment. It runs as a **single all-in-one container** with Ollama (LLM) and ChromaDB (embedded) bundled inside.

```
┌──────────────────┐     ┌──────────────────────────────────────┐
│  Forge Frontend  │────▶│         Forge Assistant               │
│  (React chat)    │ SSE │  ┌──────────┐  ┌──────────────────┐  │
└──────────────────┘     │  │  Ollama   │  │    FastAPI        │  │
                         │  │ gemma3:1b │  │  (RAG pipeline)   │  │
                         │  └──────────┘  └────────┬──────────┘  │
                         │                ┌────────▼──────────┐  │
                         │                │  ChromaDB (embed)  │  │
                         │                └───────────────────┘  │
                         └──────────────────────────────────────┘
```

## Features

- **Contextual help** — knows which page the user is on
- **Documentation search** — RAG-powered answers from indexed Forge/Ansible docs
- **Error explanation** — analyze failed job output
- **Streaming responses** — token-by-token display via Server-Sent Events
- **Privacy-first** — all data stays on your server, no cloud APIs

## Quick Start

```bash
# Start the assistant (all-in-one: Ollama + ChromaDB + FastAPI)
docker compose up -d

# Wait ~2 minutes for Ollama to load the model on first start,
# then index documentation
curl -X POST http://localhost:8100/api/v1/index

# Test it
curl -X POST http://localhost:8100/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "How do I create a job template?"}'
```

> **Note:** On first start, the entrypoint automatically pulls the LLM model (`gemma3:1b`) and embedding model (`nomic-embed-text`). The healthcheck `start_period` is 120 seconds to allow time for this.

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
| `FORGE_ASSISTANT_OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API URL (localhost — runs inside the same container) |
| `FORGE_ASSISTANT_OLLAMA_MODEL` | `gemma3:1b` | LLM model |
| `FORGE_ASSISTANT_OLLAMA_EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `FORGE_ASSISTANT_CHROMA_HOST` | `localhost` | ChromaDB host (localhost — embedded in the same container) |
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
