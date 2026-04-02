# API Reference

Base URL: `http://localhost:8100` (standalone) or `/assistant` (behind Forge nginx)

---

## Health Check

```
GET /api/v1/health
```

**Response:**
```json
{
  "status": "ok",
  "version": "2026.04.0",
  "ollama": true,
  "chromadb": true,
  "model": "mistral:7b"
}
```

| Field | Description |
|-------|-------------|
| `status` | `"ok"` if all dependencies healthy, `"degraded"` otherwise |
| `ollama` | Whether Ollama is reachable and has the configured model |
| `chromadb` | Whether ChromaDB is reachable |
| `model` | Configured LLM model name |

---

## Chat (SSE Streaming)

```
POST /api/v1/chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "How do I create a job template with survey variables?",
  "context": {
    "page": "/templates/job_template/new"
  },
  "history": [
    {"role": "user", "content": "What is a job template?"},
    {"role": "assistant", "content": "A job template defines..."}
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's question |
| `context` | object | No | Page context (`page` key with current route) |
| `history` | array | No | Previous messages (last 3 exchanges used) |

**Response:** `text/event-stream`

```
data: {"token": "To"}
data: {"token": " create"}
data: {"token": " a"}
data: {"token": " job"}
data: {"token": " template"}
data: {"token": ":"}
data: {"token": "\n\n"}
data: {"token": "1."}
data: {"token": " Navigate"}
...
data: {"done": true}
```

**Error:**
```
data: {"error": "Connection to Ollama failed", "done": true}
```

---

## Index Documents

```
POST /api/v1/index?rebuild=false
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rebuild` | bool | `false` | Delete existing index and re-index from scratch |

**Response:**
```json
{
  "indexed_chunks": 142,
  "rebuild": false
}
```

---

## OpenAPI Documentation

Interactive Swagger UI is available at:
```
GET /api/v1/docs
```

OpenAPI JSON schema:
```
GET /api/v1/openapi.json
```
