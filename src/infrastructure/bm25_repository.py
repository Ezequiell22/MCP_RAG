from rank_bm25 import BM25Okapi

from src.domain.interfaces import BM25Index
from src.domain.models import Chunk


class BM25Repository(BM25Index):
    def __init__(self):
        self.index: BM25Okapi | None = None
        self.chunk_ids: list[str] = []
        self.documents: list[str] = []

    def build(self, texts: list[str]) -> None:
        tokenized = [self._tokenize(t) for t in texts]
        self.index = BM25Okapi(tokenized)
        self.documents = texts

    def build_from_chunks(self, chunks: list[Chunk]) -> None:
        self.chunk_ids = [c.id for c in chunks]
        self.build([c.content for c in chunks])

    def search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        if not self.index:
            return []
        tokenized = self._tokenize(query)
        scores = self.index.get_scores(tokenized)
        indexed = list(enumerate(scores))
        indexed.sort(key=lambda x: -x[1])
        results: list[tuple[str, float]] = []
        for idx, score in indexed[:k]:
            if score > 0:
                cid = self.chunk_ids[idx] if idx < len(self.chunk_ids) else str(idx)
                results.append((cid, score))
        return results

    def _tokenize(self, text: str) -> list[str]:
        return text.lower().split()
