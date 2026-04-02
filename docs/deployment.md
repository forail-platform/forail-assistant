# Deployment

## Standalone Deployment

Run the assistant independently:

```bash
cd forge-assistant
docker compose up -d
```

This starts three services:
- **ollama** — LLM server on port 11434
- **chromadb** — vector store on port 8000
- **forge-assistant** — API on port 8100

### First-Time Setup

```bash
# 1. Pull LLM models (one-time, ~4 GB download)
docker compose run --rm setup

# 2. Index documentation
curl -X POST http://localhost:8100/api/v1/index

# 3. Verify
curl http://localhost:8100/api/v1/health
```

---

## Integration with Forge Platform

### Step 1: Add to Docker Compose

In your `forge-deploy` directory:

```bash
docker compose -f docker-compose.yml \
  -f /path/to/forge-assistant/docker-compose.integration.yml \
  up -d
```

### Step 2: Configure Nginx

Add to your Forge nginx configuration:

```nginx
# In forge-deploy/nginx/nginx.conf, inside the server block:
location /assistant/ {
    proxy_pass http://forge-assistant:8100/;
    proxy_http_version 1.1;
    proxy_set_header Connection '';
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # SSE support
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 300s;
}
```

### Step 3: Frontend Detection

The Forge frontend automatically detects the assistant by calling `/assistant/api/v1/health`. If the endpoint responds, the chat button appears in the UI.

---

## GPU Support

For GPU-accelerated inference, uncomment the GPU section in `docker-compose.yml`:

```yaml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Requirements:
- NVIDIA GPU with 8+ GB VRAM
- nvidia-container-toolkit installed on the host
- Docker configured with nvidia runtime

---

## CPU-Only Deployment

For servers without GPU, use a smaller model:

```bash
FORGE_ASSISTANT_OLLAMA_MODEL=phi3:mini docker compose up -d
```

Response time will be 10-20 seconds instead of 2-5 seconds.

---

## Removing the Assistant

To remove the assistant from a running Forge deployment:

```bash
# Stop assistant services
docker compose -f docker-compose.yml \
  -f /path/to/forge-assistant/docker-compose.integration.yml \
  down forge-assistant ollama chromadb

# Or if running standalone
cd forge-assistant && docker compose down -v
```

The Forge platform continues to work normally. The chat button disappears automatically when the health check fails.

---

## Backup and Restore

### ChromaDB Data

```bash
# Backup
docker compose exec chromadb tar czf /tmp/chroma-backup.tar.gz /chroma/chroma
docker compose cp chromadb:/tmp/chroma-backup.tar.gz ./backups/

# Restore
docker compose cp ./backups/chroma-backup.tar.gz chromadb:/tmp/
docker compose exec chromadb tar xzf /tmp/chroma-backup.tar.gz -C /
```

### Ollama Models

Models are stored in the `ollama_data` volume. To backup:

```bash
docker run --rm -v forge-assistant_ollama_data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/ollama-models.tar.gz /data
```

---

## CI/CD Pipeline

The included `Jenkinsfile` provides a complete pipeline:

1. **Lint** — ruff check on Python code
2. **Test** — pytest with JUnit XML reporting
3. **Build** — Docker image build
4. **Scan** — Trivy container vulnerability scan
5. **Push** — Push to Harbor registry (main branch only)
6. **Deploy** — SSH deploy to production (main branch only)

Tests must pass before any image is built or pushed.
