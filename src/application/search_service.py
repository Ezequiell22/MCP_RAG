import hashlib
import time

from src.config.settings import Settings
from src.domain.models import ChunkResult
from src.infrastructure.bm25_repository import BM25Repository
from src.infrastructure.chromadb_repository import ChromaRepository
from src.infrastructure.embedding_provider import HuggingFaceEmbeddingProvider

RRF_K = 60


class _CacheEntry:
    def __init__(self, value: list[ChunkResult]):
        self.value = value
        self.timestamp = time.monotonic()


class SearchService:
    def __init__(self, settings: Settings, vector_store: ChromaRepository | None = None, bm25: BM25Repository | None = None, embedding_provider: HuggingFaceEmbeddingProvider | None = None):
        self.settings = settings
        self.vector_store = vector_store
        self.bm25 = bm25
        self.embedding_provider = embedding_provider or HuggingFaceEmbeddingProvider(settings.embedding.model)
        self._cache: dict[str, _CacheEntry] = {}
        self.log = None

    def set_logger(self, logger):
        self.log = logger

    def search(self, query: str, k: int | None = None, fonte: str | None = None) -> list[ChunkResult]:
        k = k or self.settings.search.top_k
        cache_key = hashlib.sha256(f"{query}:{fonte}".encode()).hexdigest()

        cached = self._cache.get(cache_key)
        if cached:
            age = time.monotonic() - cached.timestamp
            if age < self.settings.search.cache_ttl:
                if self.log: self.log.info("Cache hit for query: %s", query[:60])
                return cached.value[:k]
            else:
                del self._cache[cache_key]

        where = {"fonte": fonte} if fonte else None
        query_emb = self.embedding_provider.embed_query(query)
        vector_results = self.vector_store.similarity_search(query_emb, k=k * 2, where=where)

        if self.settings.search.hybrid and not where:
            bm25_results = self.bm25.search(query, k=k * 2)
            if bm25_results:
                vector_results = self._rrf_merge(vector_results, bm25_results)

        result = vector_results[:k]

        if len(self._cache) >= self.settings.search.cache_max_size:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k].timestamp)
            del self._cache[oldest]

        self._cache[cache_key] = _CacheEntry(result)
        return result

    def _rrf_merge(
        self, vector_results: list[ChunkResult], bm25_results: list[tuple[str, float]]
    ) -> list[ChunkResult]:
        scores: dict[str, float] = {}
        results_by_id: dict[str, ChunkResult] = {}

        for rank, doc in enumerate(vector_results):
            doc_id = doc.id or str(id(doc))
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (RRF_K + rank + 1)
            results_by_id[doc_id] = doc

        for rank, (doc_id, _) in enumerate(bm25_results):
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (RRF_K + rank + 1)

        ranked_ids = sorted(scores.keys(), key=lambda i: -scores[i])
        ranked = [results_by_id[i] for i in ranked_ids if i in results_by_id]
        return ranked

    def clear_cache(self) -> None:
        self._cache.clear()
