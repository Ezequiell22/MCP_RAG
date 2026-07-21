from pathlib import Path
from tempfile import NamedTemporaryFile

from src.infrastructure.markdown_loader import MarkdownLoader


def test_markdown_loader_simple():
    loader = MarkdownLoader()
    with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# Title\n\nHello world")
        p = Path(f.name)
    assert loader.supports(p)
    doc = loader.load(p, source_dir=p.parent, source_type="test")
    assert doc["path"] == p.name
    assert doc["fonte"] == "test"
    assert doc["secoes"] == []
    p.unlink()


def test_markdown_loader_frontmatter():
    loader = MarkdownLoader()
    content = """---
descricao: "My Doc"
palavras_chave: [a, b, c]
---
# Title

Body
"""
    with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        p = Path(f.name)
    doc = loader.load(p, source_dir=p.parent)
    assert doc["descricao"] == "My Doc"
    assert doc["palavras_chave"] == ["a", "b", "c"]
    p.unlink()


def test_markdown_loader_sections():
    loader = MarkdownLoader()
    content = "# T\n\n## Sec1\n\nx\n\n## Sec2\n\ny"
    with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        p = Path(f.name)
    doc = loader.load(p, source_dir=p.parent)
    assert doc["secoes"] == ["Sec1", "Sec2"]
    p.unlink()
