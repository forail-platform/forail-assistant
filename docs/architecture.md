# Architecture

## Overview

Forail Assistant is a standalone microservice that provides AI-powered help for the Forail platform. It uses Retrieval-Augmented Generation (RAG) to answer questions based on indexed documentation.

```
                    ┌─────────────────────────────────┐
                    │         Forail Frontend           │
                    │  (React chat panel component)    │
                    └───────────────┬──────────────────┘
                                    │ SSE (Server-Sent Events)
                                    ▼
                    ┌─────────────────────────────────┐
                    │   Forail Assistant (all-in-one)   │
                    │                                  │
                    │  FastAPI  /api/v1/chat  → SSE    │
                    │           /api/v1/health→ JSON   │
                    │           /api/v1/index → reindex│
                    │                                  │
                    │  Ollama   gemma3:1b (LLM)        │
                    │           nomic-embed-text (emb)  │
                    │                                  │
                    │  ChromaDB (embedded vector store) │
                    └─────────────────────────────────┘
```

> **Note:** All three components (FastAPI, Ollama, ChromaDB) run inside a single Docker container. The entrypoint script starts Ollama and ChromaDB as background processes before launching the FastAPI server.

## Components

### FastAPI Application (`app/`)

The core service, responsible for:

- Receiving chat requests with optional page context and history
- Querying ChromaDB for relevant documentation chunks
- Building a context-enriched prompt for the LLM
- Streaming the response token-by-token via SSE

**Key files:**
- `app/main.py` — FastAPI app, endpoints, CORS
- `app/rag.py` — RAG pipeline (embed, retrieve, generate, stream)
- `app/indexer.py` — Document loading, chunking, indexing
- `app/config.py` — Pydantic settings from environment

### Ollama (LLM Server)

Runs the language model locally inside the same container. Two models are used:
- **gemma3:1b** (default, or configured model) — for chat generation
- **nomic-embed-text** — for generating document/query embeddings

The Ollama binary is copied from the official `ollama/ollama` image at build time. GPU acceleration is optional but recommended for larger models.

### ChromaDB (Vector Store)

Stores document chunks as vectors for similarity search. When a user asks a question:
1. The question is embedded using `nomic-embed-text`
2. ChromaDB finds the top-K most similar document chunks
3. These chunks become the context for the LLM

## Data Flow

### Chat Request

```
1. User types "How do I create a scheduled job?"
2. Frontend sends POST /api/v1/chat with message + page context
3. Assistant embeds the question via Ollama /api/embeddings
4. Assistant queries ChromaDB for top 5 relevant doc chunks
5. Assistant builds system prompt with doc context
6. Assistant streams response from Ollama /api/chat
7. Each token is sent to frontend as SSE data event
8. Frontend renders tokens in real-time
```

### Document Indexing

```
1. Admin calls POST /api/v1/index (or runs indexer script)
2. Indexer reads all .md files from docs_to_index/
3. Each file is split into overlapping chunks (500 chars, 50 overlap)
4. Each chunk is embedded via Ollama nomic-embed-text
5. Embeddings + text stored in ChromaDB collection "forail_docs"
```

## Design Decisions

### Why Standalone Service (Not Django App)?

- **No Django dependency** — FastAPI is lighter, async-native, no ORM needed
- **Optional** — can be added/removed without touching core Forail
- **Independent scaling** — can run on a separate GPU server
- **Independent release cycle** — update models without redeploying Forail

### Why Ollama (Not OpenAI/Claude API)?

- **Privacy** — all data stays on your infrastructure
- **Cost** — no API fees, no usage limits
- **Offline** — works without internet
- **Control** — choose and swap models freely

### Why FastAPI (Not Flask/Django)?

- **Native async** — SSE streaming without workarounds
- **Fast** — ASGI, built on Starlette
- **Auto docs** — OpenAPI schema generated automatically
- **Minimal** — no ORM, no admin, no migrations needed

### Why ChromaDB (Not Pinecone/Weaviate)?

- **Local** — no cloud dependency
- **Python-native** — simple API, no external clients
- **Lightweight** — single container, ~500MB
- **Good enough** — for <100K document chunks, ChromaDB performs well
