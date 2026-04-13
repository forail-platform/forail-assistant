"""Shared ChromaDB client and embedding helpers."""

import logging

import chromadb
import httpx

from app.config import settings

logger = logging.getLogger(__name__)

_chroma_client = None
_collection = None


def get_chroma_client():
    """Lazy-initialize ChromaDB HTTP client (singleton)."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
        )
    return _chroma_client


def get_chroma_collection():
    """Lazy-initialize ChromaDB collection (singleton)."""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def reset_collection():
    """Delete and recreate the collection (for rebuild)."""
    global _collection
    client = get_chroma_client()
    try:
        client.delete_collection(settings.chroma_collection)
        logger.info("Deleted existing collection: %s", settings.chroma_collection)
    except Exception:
        pass
    _collection = client.get_or_create_collection(
        name=settings.chroma_collection,
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


async def get_embedding(text: str) -> list[float]:
    """Generate embedding using Ollama (async)."""
    async with httpx.AsyncClient(timeout=settings.ollama_timeout) as client:
        resp = await client.post(
            f"{settings.ollama_base_url}/api/embeddings",
            json={"model": settings.ollama_embed_model, "prompt": text},
        )
        resp.raise_for_status()
        return resp.json()["embedding"]


def get_embedding_sync(text: str) -> list[float]:
    """Generate embedding using Ollama (synchronous, for indexing)."""
    resp = httpx.post(
        f"{settings.ollama_base_url}/api/embeddings",
        json={"model": settings.ollama_embed_model, "prompt": text},
        timeout=settings.ollama_timeout,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]
