import pytest

from src.config.settings import ChunkingConfig
from src.infrastructure.splitter import split_markdown


def test_splitter_creates_chunks_per_section():
    text = "# Title\n\nintro\n\n## Section One\n\ncontent a\n\n### Sub\n\nsub content\n\n## Section Two\n\ncontent b"
    config = ChunkingConfig(max_size=5000, overlap=0)
    chunks = split_markdown(text, "test.md", {}, config)
    assert len(chunks) >= 2
    sections = [c.metadata["section"] for c in chunks]
    assert "Section One" in sections
    assert "Section Two" in sections


def test_splitter_without_headings():
    text = "just a plain paragraph\n\nwith multiple lines"
    config = ChunkingConfig(max_size=5000, overlap=0)
    chunks = split_markdown(text, "plain.md", {}, config)
    assert len(chunks) == 1
    assert chunks[0].metadata["section"] == "Introdução"


def test_splitter_respects_max_size():
    long_text = "# Title\n\n" + "## Section\n\n" + "word " * 2000
    config = ChunkingConfig(max_size=500, overlap=50)
    chunks = split_markdown(long_text, "long.md", {}, config)
    assert all(len(c.content) <= 500 for c in chunks)
    assert len(chunks) > 1


def test_splitter_preserves_metadata():
    meta = {"fonte": "test", "path": "doc.md"}
    text = "## A\n\ncontent\n\n## B\n\nmore"
    config = ChunkingConfig(max_size=5000, overlap=0)
    chunks = split_markdown(text, "doc.md", meta, config)
    for c in chunks:
        assert c.metadata["fonte"] == "test"
