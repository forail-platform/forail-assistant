"""Tests for document indexer."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.indexer import chunk_text, load_documents


class TestChunkText:

    def test_short_text(self):
        chunks = chunk_text("Hello world", chunk_size=100, overlap=10)
        assert chunks == ["Hello world"]

    def test_exact_chunk(self):
        text = "A" * 100
        chunks = chunk_text(text, chunk_size=100, overlap=0)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_splits_long_text(self):
        text = "A" * 250
        chunks = chunk_text(text, chunk_size=100, overlap=20)
        assert len(chunks) >= 3
        for chunk in chunks:
            assert len(chunk) <= 100

    def test_overlap_works(self):
        text = "AABBCCDDEE" * 10  # 100 chars
        chunks = chunk_text(text, chunk_size=30, overlap=10)
        # With overlap, chunks should share characters
        assert len(chunks) >= 4

    def test_empty_text(self):
        chunks = chunk_text("", chunk_size=100, overlap=10)
        assert chunks == []

    def test_whitespace_only(self):
        chunks = chunk_text("   \n\n   ", chunk_size=100, overlap=10)
        assert chunks == []


class TestLoadDocuments:

    def test_loads_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            (p / "guide.md").write_text("# Guide\nSome content")
            (p / "api.md").write_text("# API\nEndpoints")
            (p / "subdir").mkdir()
            (p / "subdir" / "nested.md").write_text("# Nested\nContent")
            (p / "ignored.txt").write_text("Not markdown")

            docs = load_documents(p)
            assert len(docs) == 3
            paths = [d["path"] for d in docs]
            assert "guide.md" in paths
            assert "api.md" in paths

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = load_documents(Path(tmpdir))
            assert docs == []

    def test_nonexistent_directory(self):
        docs = load_documents(Path("/nonexistent"))
        assert docs == []

    def test_skips_empty_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            (p / "empty.md").write_text("")
            (p / "content.md").write_text("Has content")

            docs = load_documents(p)
            assert len(docs) == 1
            assert docs[0]["path"] == "content.md"
