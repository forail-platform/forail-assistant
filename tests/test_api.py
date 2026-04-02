"""Tests for FastAPI endpoints."""

import json
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:

    def test_health_ok(self, client):
        with patch("app.main.check_ollama_health", new_callable=AsyncMock, return_value=True), \
             patch("app.main.check_chroma_health", new_callable=AsyncMock, return_value=True):
            resp = client.get("/api/v1/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "ok"
            assert data["ollama"] is True
            assert data["chromadb"] is True
            assert "version" in data
            assert "model" in data

    def test_health_degraded(self, client):
        with patch("app.main.check_ollama_health", new_callable=AsyncMock, return_value=False), \
             patch("app.main.check_chroma_health", new_callable=AsyncMock, return_value=True):
            resp = client.get("/api/v1/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "degraded"
            assert data["ollama"] is False

    def test_health_all_down(self, client):
        with patch("app.main.check_ollama_health", new_callable=AsyncMock, return_value=False), \
             patch("app.main.check_chroma_health", new_callable=AsyncMock, return_value=False):
            resp = client.get("/api/v1/health")
            data = resp.json()
            assert data["status"] == "degraded"
            assert data["ollama"] is False
            assert data["chromadb"] is False


class TestChatEndpoint:

    def test_chat_streams_tokens(self, client):
        async def mock_stream(*args, **kwargs):
            for token in ["Hello", " ", "world", "!"]:
                yield token

        with patch("app.main.stream_chat", side_effect=mock_stream):
            resp = client.post(
                "/api/v1/chat",
                json={"message": "Hi"},
            )
            assert resp.status_code == 200
            assert "text/event-stream" in resp.headers["content-type"]

            # Parse SSE events
            tokens = []
            for line in resp.text.strip().split("\n"):
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "token" in data:
                        tokens.append(data["token"])
                    if data.get("done"):
                        break

            assert "Hello" in tokens
            assert "world" in tokens

    def test_chat_with_context(self, client):
        async def mock_stream(*args, **kwargs):
            yield "OK"

        with patch("app.main.stream_chat", side_effect=mock_stream) as mock:
            resp = client.post(
                "/api/v1/chat",
                json={
                    "message": "How to create a template?",
                    "context": {"page": "/templates"},
                    "history": [
                        {"role": "user", "content": "Hello"},
                        {"role": "assistant", "content": "Hi!"},
                    ],
                },
            )
            assert resp.status_code == 200

    def test_chat_empty_message_rejected(self, client):
        resp = client.post("/api/v1/chat", json={})
        assert resp.status_code == 422  # Validation error

    def test_chat_error_handling(self, client):
        async def mock_stream(*args, **kwargs):
            raise Exception("LLM error")
            yield  # Make it a generator

        with patch("app.main.stream_chat", side_effect=mock_stream):
            resp = client.post(
                "/api/v1/chat",
                json={"message": "test"},
            )
            assert resp.status_code == 200
            # Should contain error in stream
            assert "error" in resp.text or "done" in resp.text


class TestIndexEndpoint:

    def test_index_trigger(self, client):
        with patch("app.indexer.index_documents", return_value=42):
            resp = client.post("/api/v1/index")
            assert resp.status_code == 200
            data = resp.json()
            assert data["indexed_chunks"] == 42
            assert data["rebuild"] is False

    def test_index_rebuild(self, client):
        with patch("app.indexer.index_documents", return_value=100):
            resp = client.post("/api/v1/index?rebuild=true")
            assert resp.status_code == 200
            data = resp.json()
            assert data["rebuild"] is True


class TestOpenAPI:

    def test_docs_available(self, client):
        resp = client.get("/api/v1/docs")
        assert resp.status_code == 200

    def test_openapi_schema(self, client):
        resp = client.get("/api/v1/openapi.json")
        assert resp.status_code == 200
        schema = resp.json()
        assert "/api/v1/health" in schema["paths"]
        assert "/api/v1/chat" in schema["paths"]
