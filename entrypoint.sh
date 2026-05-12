#!/bin/bash
set -e

echo "==> Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "==> Waiting for Ollama..."
until curl -sf http://localhost:11434/ > /dev/null 2>&1; do
    sleep 1
done
echo "==> Ollama ready."

# Pull models if not present
if ! ollama list 2>/dev/null | grep -q "${FORGE_ASSISTANT_OLLAMA_MODEL:-mistral:7b}"; then
    echo "==> Pulling model ${FORGE_ASSISTANT_OLLAMA_MODEL:-mistral:7b}..."
    ollama pull "${FORGE_ASSISTANT_OLLAMA_MODEL:-mistral:7b}"
fi

if ! ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
    echo "==> Pulling embedding model nomic-embed-text..."
    ollama pull nomic-embed-text
fi

echo "==> Starting ChromaDB..."
chroma run --host 0.0.0.0 --port 8000 --path /data/chroma > /dev/null 2>&1 &
CHROMA_PID=$!

# Wait for ChromaDB
echo "==> Waiting for ChromaDB..."
until curl -sf http://localhost:8000/api/v2/heartbeat > /dev/null 2>&1; do
    sleep 1
done
echo "==> ChromaDB ready."

# Index documents on first start
echo "==> Indexing documentation..."
cd /app && python -c "from app.indexer import index_documents; count = index_documents(); print(f'Indexed {count} chunks')"

echo "==> Starting Forge Assistant API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8100
