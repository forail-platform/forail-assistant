"""Document indexer for ChromaDB RAG pipeline.

Reads markdown files from docs_to_index/ directory, splits them into chunks,
generates embeddings via Ollama, and stores in ChromaDB.
"""

import hashlib
import logging
import os
from pathlib import Path

from app.config import settings
from app.db import get_chroma_collection, reset_collection, get_embedding_sync

logger = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.parent / "docs_to_index"


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """Split text into overlapping chunks by character count."""
    if chunk_size is None:
        chunk_size = settings.rag_chunk_size
    if overlap is None:
        overlap = settings.rag_chunk_overlap

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks




def load_documents(docs_dir: Path = None) -> list[dict]:
    """Load all markdown files from docs directory."""
    if docs_dir is None:
        docs_dir = DOCS_DIR

    documents = []
    if not docs_dir.exists():
        logger.warning("Docs directory does not exist: %s", docs_dir)
        return documents

    for md_file in sorted(docs_dir.rglob("*.md")):
        relative_path = md_file.relative_to(docs_dir)
        content = md_file.read_text(encoding="utf-8")
        if content.strip():
            documents.append({
                "path": str(relative_path),
                "content": content,
            })
            logger.info("Loaded: %s (%d chars)", relative_path, len(content))

    return documents


def index_documents(rebuild: bool = False):
    """Index all documents into ChromaDB.

    Args:
        rebuild: If True, delete existing collection and re-index everything.
    """
    if rebuild:
        collection = reset_collection()
    else:
        collection = get_chroma_collection()

    documents = load_documents()
    if not documents:
        logger.warning("No documents found to index")
        return 0

    total_chunks = 0

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            doc_id = hashlib.md5(f"{doc['path']}::{i}".encode()).hexdigest()

            try:
                embedding = get_embedding_sync(chunk)
                collection.upsert(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{"source": doc["path"], "chunk_index": i}],
                )
                total_chunks += 1
            except Exception:
                logger.exception("Failed to index chunk %d of %s", i, doc["path"])

    logger.info("Indexed %d chunks from %d documents", total_chunks, len(documents))
    return total_chunks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    count = index_documents(rebuild="--rebuild" in os.sys.argv)
    print(f"Indexed {count} chunks")
