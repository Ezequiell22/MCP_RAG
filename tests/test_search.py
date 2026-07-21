from src.application.search_service import SearchService
from src.config.settings import Settings


def test_rrf_merge():
    from src.domain.models import ChunkResult
    s = SearchService(Settings())
    v = [
        ChunkResult(id="a", arquivo="a.md", titulo="A", score=0.9, conteudo="x"),
        ChunkResult(id="b", arquivo="b.md", titulo="B", score=0.8, conteudo="y"),
        ChunkResult(id="c", arquivo="c.md", titulo="C", score=0.7, conteudo="z"),
    ]
    bm = [("c", 0.9), ("b", 0.5)]

    merged = s._rrf_merge(v, bm)
    ids = [m.id for m in merged]
    assert ids[0] == "c"  # c: vec_rrf(1/62) + bm_rrf(1/61) = higher than others


def test_empty_search():
    s = SearchService(Settings(), vector_store=None, bm25=None)
    s.vector_store = type("Mock", (), {"similarity_search": lambda self, q, k=5, where=None: []})()
    s.bm25 = type("Mock", (), {"search": lambda self, q, k=5: []})()
    results = s.search("test query")
    assert results == []
