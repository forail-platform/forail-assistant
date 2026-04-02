"""Application configuration from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "mistral:7b"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_timeout: int = 120

    # ChromaDB
    chroma_host: str = "chromadb"
    chroma_port: int = 8000
    chroma_collection: str = "forge_docs"

    # RAG
    rag_top_k: int = 5
    rag_chunk_size: int = 500
    rag_chunk_overlap: int = 50

    # App
    app_name: str = "Forge Assistant"
    app_version: str = "2026.04.0"
    log_level: str = "INFO"
    cors_origins: str = "*"

    model_config = {"env_prefix": "FORGE_ASSISTANT_"}


settings = Settings()
