### Forge Assistant — All-in-one image
### Ollama (LLM) + ChromaDB (embedded) + FastAPI in a single container

FROM ollama/ollama:latest AS ollama

FROM python:3.12-slim

# System deps for ChromaDB (sqlite3, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Ollama binary from official image
COPY --from=ollama /bin/ollama /usr/local/bin/ollama

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY docs_to_index/ ./docs_to_index/

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Directories for data persistence
RUN mkdir -p /data/ollama /data/chroma

ENV OLLAMA_MODELS=/data/ollama
ENV FORGE_ASSISTANT_OLLAMA_BASE_URL=http://localhost:11434
ENV FORGE_ASSISTANT_OLLAMA_MODEL=gemma3:1b
ENV FORGE_ASSISTANT_CHROMA_HOST=localhost
ENV FORGE_ASSISTANT_CHROMA_PORT=8000
ENV FORGE_ASSISTANT_LOG_LEVEL=INFO

EXPOSE 8100

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -sf http://localhost:8100/api/v1/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
