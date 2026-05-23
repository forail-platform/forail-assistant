# Deployment

## Standalone Deployment

Run the assistant independently:

```bash
cd forge-assistant
docker compose up -d
```

This starts a **single all-in-one container** (`forge-assistant`) that bundles:
- **Ollama** — LLM server (internal, port 11434)
- **ChromaDB** — vector store (embedded, port 8000)
- **FastAPI** — API server (exposed on port 8100)

### First-Time Setup

On first start, the entrypoint automatically pulls the LLM model (`gemma3:1b`) and embedding model (`nomic-embed-text`). Allow ~2 minutes for the initial model download.

```bash
# 1. Start the container
docker compose up -d

# 2. Wait for health check to pass (start_period is 120s)
docker compose logs -f forge-assistant

# 3. Index documentation
curl -X POST http://localhost:8100/api/v1/index

# 4. Verify
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
  forge-assistant:
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
# Stop assistant service
docker compose -f docker-compose.yml \
  -f /path/to/forge-assistant/docker-compose.integration.yml \
  down forge-assistant

# Or if running standalone
cd forge-assistant && docker compose down -v
```

The Forge platform continues to work normally. The chat button disappears automatically when the health check fails.

---

## Backup and Restore

All persistent data (ChromaDB + Ollama models) is stored in the `assistant_data` volume mounted at `/data`:

```bash
# Backup
docker run --rm -v forge-assistant_assistant_data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/assistant-data.tar.gz /data

# Restore
docker run --rm -v forge-assistant_assistant_data:/data -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/assistant-data.tar.gz -C /
```

> **Tip:** Re-indexing docs (`curl -X POST http://localhost:8100/api/v1/index?rebuild=true`) is fast and often easier than restoring ChromaDB data. Model re-download is automatic on first start if models are missing.

---

## CI/CD Pipeline

The repository ships with a **GitHub Actions** workflow in `.github/workflows/ci.yml`:

1. **Lint** — ruff check on Python code
2. **Test** — pytest with JUnit XML reporting
3. **Build** — Docker image build
4. **Scan** — Trivy container vulnerability scan
5. **Push** — Push to `ghcr.io/forgeplatform/forge-assistant` (main branch and version tags only)

Tests must pass before any image is built or pushed. Releases use the built-in `GITHUB_TOKEN` with `packages: write` — no external secrets required.
