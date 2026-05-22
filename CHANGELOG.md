# Changelog

All notable changes to the Forge Assistant will be documented in this file.

## [Unreleased]

## [2026.05.0] - 2026-05-22

### Changed
- Switched to an all-in-one Docker image bundling Ollama, ChromaDB (embedded), and the FastAPI service in one container. `docker-compose.yml` collapsed from three services + setup container to a single service with one `/data` volume.
- Default Ollama model changed from `mistral:7b` to `gemma3:1b` (smaller and faster; reduced answer quality for general questions but adequate for short RAG-grounded responses).
- Default Ollama timeout raised from 120s to 300s, and the httpx client now uses an explicit `Timeout(connect=10, read=300, write=10, pool=10)` so the long read timeout no longer applies to connection setup.
- Default RAG `top_k` lowered from 5 to 3.
- Default config hosts switched from `ollama` / `chromadb` (Compose hostnames) to `localhost` to match the single-container layout.
- Container healthcheck now uses `curl` with `start_period=120s` to accommodate model-pull on first boot.

### Added
- `entrypoint.sh` orchestrates startup: `ollama serve`, conditional model pull (configurable model + `nomic-embed-text`), `chroma run`, document indexing, then `uvicorn`.
- Deployment documentation in `docs_to_index/deployment/` (architecture overview, Docker deployment, CI/CD pipeline, contributing guide, admin/user handbooks, release notes, startup walkthrough) so the RAG index can answer operational questions.

## [2026.04.0] - 2026-04-02

### Added
- Initial release of Forge Assistant as a standalone service
- FastAPI application with SSE streaming chat endpoint
- RAG pipeline: ChromaDB vector retrieval + Ollama LLM generation
- Document indexer for markdown files with configurable chunking
- Health check endpoint reporting Ollama and ChromaDB status
- Docker Compose configuration with Ollama, ChromaDB, and Assistant services
- Integration overlay for plugging into existing Forge deployments
- Jenkinsfile with lint, test, build, scan, push, and deploy stages
- 29 unit/integration tests covering API, config, indexer, and RAG
- System prompt with honesty constraints and markdown formatting
- Context-aware chat: passes current page location to the LLM
- Conversation history support (last 3 exchanges)
- Environment-based configuration with `FORGE_ASSISTANT_` prefix
- Complete documentation: architecture, API reference, configuration, deployment
