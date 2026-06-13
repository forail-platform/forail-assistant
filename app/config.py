"""Application configuration from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:1b"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_timeout: int = 300

    # ChromaDB
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_collection: str = "forail_docs"

    # RAG
    rag_top_k: int = 3
    rag_chunk_size: int = 500
    rag_chunk_overlap: int = 50

    # App
    app_name: str = "Forail Assistant"
    app_version: str = "2026.06.0"
    log_level: str = "INFO"
    cors_origins: str = "*"

    # Admin token required to call the re-indexing endpoint. When empty the
    # endpoint is disabled (fail closed). Startup auto-indexing is unaffected.
    admin_token: str = ""

    model_config = {"env_prefix": "FORAIL_ASSISTANT_"}


settings = Settings()
