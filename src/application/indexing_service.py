import hashlib
import json
from pathlib import Path

from src.config.settings import Settings, SourceConfig
from src.domain.models import Chunk
from src.infrastructure.bm25_repository import BM25Repository
from src.infrastructure.chromadb_repository import ChromaRepository
from src.infrastructure.embedding_provider import HuggingFaceEmbeddingProvider
from src.infrastructure.markdown_loader import MarkdownLoader
from src.infrastructure.splitter import split_markdown
from src.infrastructure.text_loader import TextLoader


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_loader_chain() -> list:
    return [MarkdownLoader(), TextLoader()]


def _find_files(source_dir: Path, loaders: list) -> list[tuple[Path]]:
    files = []
    for pattern in ("**/*",):
        for fpath in sorted(source_dir.glob(pattern)):
            if fpath.is_file() and any(loader.supports(fpath) for loader in loaders):
                files.append(fpath)
    return files


class IndexingService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.vector_store = ChromaRepository(str(settings.db_path), settings.collection_name)
        self.bm25 = BM25Repository()
        self.embedding_provider = HuggingFaceEmbeddingProvider(
            settings.embedding.model
        )
        self.loaders = _build_loader_chain()
        self.log = None

    def set_logger(self, logger):
        self.log = logger

    def _hash_path(self) -> Path:
        return Path(str(self.settings.db_path)) / ".index_hash.json"

    def _load_hashes(self) -> dict[str, str]:
        f = self._hash_path()
        if f.exists():
            return json.loads(f.read_text())
        return {}

    def _save_hashes(self, hashes: dict[str, str]) -> None:
        f = self._hash_path()
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(hashes, indent=2))

    def index_all(self) -> None:
        log = self.log
        sources = self.settings.resolve_sources()
        if not sources:
            if log: log.warning("No sources configured")
            return

        force_rebuild = self.vector_store.count() == 0
        previous_hashes = self._load_hashes() if not force_rebuild else {}
        current_hashes: dict[str, str] = {}
        all_chunks: list[Chunk] = []

        for source in sources:
            source_dir = Path(source.path)
            if not source_dir.exists():
                if log: log.warning("Source dir %s not found", source_dir)
                continue

            for fpath in _find_files(source_dir, self.loaders):
                rel = str(fpath.relative_to(source_dir))
                h = _file_hash(fpath)
                current_hashes[f"{source.type}:{rel}"] = h

                if not force_rebuild:
                    key = f"{source.type}:{rel}"
                    if key in previous_hashes and previous_hashes[key] == h:
                        if log: log.info("Skipping %s (unchanged)", rel)
                        continue

                loader = next((l for l in self.loaders if l.supports(fpath)), None)
                if not loader:
                    continue

                try:
                    doc = loader.load(fpath, source_dir, source.type)
                except Exception as e:
                    if log: log.error("Failed to load %s: %s", rel, e)
                    continue

                meta = {
                    "path": doc["path"],
                    "fonte": doc["fonte"],
                    "descricao": doc["descricao"],
                    "palavras_chave": json.dumps(doc["palavras_chave"]),
                }

                file_chunks = split_markdown(doc["content"], doc["path"], meta, self.settings.chunking)
                all_chunks.extend(file_chunks)

                if log: log.info("Indexed %d chunks from %s [%s]", len(file_chunks), rel, source.type)

        if not all_chunks:
            if force_rebuild:
                if log: log.warning("No chunks generated from any source")
            else:
                if log: log.info("No changes detected")
            return

        texts = [c.content for c in all_chunks]
        if log: log.info("Generating embeddings for %d chunks...", len(texts))
        embeddings = self.embedding_provider.embed_documents(texts)

        self.vector_store.delete_all()
        self.vector_store.add_chunks(all_chunks, embeddings)
        self.bm25.build_from_chunks(all_chunks)

        self._save_hashes(current_hashes)
        if log: log.info("Indexed %d chunks total", self.vector_store.count())
