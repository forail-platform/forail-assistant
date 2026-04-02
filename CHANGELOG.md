# Changelog

All notable changes to the Forge Assistant will be documented in this file.

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
