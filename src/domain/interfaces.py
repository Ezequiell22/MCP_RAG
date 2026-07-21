from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.models import Chunk, ChunkResult


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    @abstractmethod
    def embed_query(self, text: str) -> list[float]: ...


class VectorStore(ABC):
    @abstractmethod
    def add_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...

    @abstractmethod
    def similarity_search(self, query_embedding: list[float], k: int = 5, where: dict | None = None) -> list[ChunkResult]: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def delete_all(self) -> None: ...


class BM25Index(ABC):
    @abstractmethod
    def build(self, texts: list[str]) -> None: ...

    @abstractmethod
    def search(self, query: str, k: int = 5) -> list[tuple[str, float]]: ...


class DocumentLoader(ABC):
    @abstractmethod
    def supports(self, path: Path) -> bool: ...

    @abstractmethod
    def load(self, path: Path, source_dir: Path | None = None, source_type: str = "documento") -> dict: ...
