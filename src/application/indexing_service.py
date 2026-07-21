import hashlib
import json
from pathlib import Path

from src.config.settings import Settings
from src.domain.models import Chunk
from src.infrastructure.bm25_repository import BM25Repository
from src.infrastructure.chromadb_repository import ChromaRepository
from src.infrastructure.embedding_provider import HuggingFaceEmbeddingProvider
from src.infrastructure.markdown_loader import load_guide
from src.infrastructure.splitter import split_markdown

HASH_FILE = ".index_hash.json"


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_hashes() -> dict[str, str]:
    f = Path(HASH_FILE)
    if f.exists():
        return json.loads(f.read_text())
    return {}


def _save_hashes(hashes: dict[str, str]) -> None:
    Path(HASH_FILE).write_text(json.dumps(hashes, indent=2))


class IndexingService:
    def __init__(self, settings: Settings):
        self.settings = settings
        emb_provider = HuggingFaceEmbeddingProvider(
            settings.embedding.model
        )
        self.vector_store = ChromaRepository(str(settings.db_path))
        self.bm25 = BM25Repository()
        self.embedding_provider = emb_provider
        self.log = None

    def set_logger(self, logger):
        self.log = logger

    def index_all(self) -> None:
        log = self.log
        guides_dir = Path(self.settings.guides_dir)
        if not guides_dir.exists():
            if log: log.warning("Guides dir %s not found", guides_dir)
            return

        md_files = sorted(guides_dir.rglob("*.md"))
        if not md_files:
            if log: log.warning("No .md files found in %s", guides_dir)
            return

        force_rebuild = self.vector_store.count() == 0
        previous_hashes = _load_hashes() if not force_rebuild else {}
        current_hashes: dict[str, str] = {}
        all_chunks: list[Chunk] = []

        for md_path in md_files:
            rel = str(md_path.relative_to(guides_dir))
            h = _file_hash(md_path)
            current_hashes[rel] = h

            if not force_rebuild and rel in previous_hashes and previous_hashes[rel] == h:
                if log: log.info("Skipping %s (unchanged)", rel)
                continue

            try:
                guide = load_guide(md_path, guides_dir)
            except Exception as e:
                if log: log.error("Failed to load %s: %s", rel, e)
                continue

            meta = {
                "path": guide["path"],
                "descricao": guide["descricao"],
                "palavras_chave": json.dumps(guide["palavras_chave"]),
            }

            chunks = split_markdown(guide["content"], guide["path"], meta, self.settings.chunking)
            all_chunks.extend(chunks)

            if log: log.info("Indexed %d chunks from %s", len(chunks), rel)

        if not all_chunks:
            if force_rebuild:
                if log: log.warning("No chunks generated from any file")
            else:
                if log: log.info("No changes detected")
            return

        texts = [c.content for c in all_chunks]
        if log: log.info("Generating embeddings for %d chunks...", len(texts))
        embeddings = self.embedding_provider.embed_documents(texts)

        self.vector_store.delete_all()
        self.vector_store.add_chunks(all_chunks, embeddings)
        self.bm25.build_from_chunks(all_chunks)

        _save_hashes(current_hashes)
        if log: log.info("Indexed %d chunks total", self.vector_store.count())
