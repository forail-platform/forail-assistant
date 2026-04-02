"""Tests for RAG pipeline."""

from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from app.rag import build_system_prompt


class TestBuildSystemPrompt:

    def test_with_docs(self):
        prompt = build_system_prompt(["Doc chunk 1", "Doc chunk 2"])
        assert "Forge Assistant" in prompt
        assert "Doc chunk 1" in prompt
        assert "Doc chunk 2" in prompt

    def test_without_docs(self):
        prompt = build_system_prompt([])
        assert "No documentation context available" in prompt

    def test_with_page_context(self):
        prompt = build_system_prompt(["Some doc"], page_context="/templates")
        assert "/templates" in prompt

    def test_without_page_context(self):
        prompt = build_system_prompt(["Some doc"])
        assert "currently on page" not in prompt

    def test_markdown_instruction(self):
        prompt = build_system_prompt(["doc"])
        assert "markdown" in prompt.lower()

    def test_honesty_instruction(self):
        prompt = build_system_prompt(["doc"])
        assert "do not make things up" in prompt.lower()
