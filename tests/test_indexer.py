from pathlib import Path
from tempfile import TemporaryDirectory

from src.application.indexing_service import _file_hash


def test_file_hash_is_consistent():
    with TemporaryDirectory() as tmp:
        f = Path(tmp) / "test.md"
        f.write_text("hello")
        h1 = _file_hash(f)
        h2 = _file_hash(f)
        assert h1 == h2


def test_file_hash_changes_with_content():
    with TemporaryDirectory() as tmp:
        f = Path(tmp) / "test.md"
        f.write_text("hello")
        h1 = _file_hash(f)
        f.write_text("world")
        h2 = _file_hash(f)
        assert h1 != h2
