from src.infrastructure.embedding_provider import (
    HuggingFaceEmbeddingProvider,
)


def test_huggingface_embed_query():
    provider = HuggingFaceEmbeddingProvider("all-MiniLM-L6-v2")
    vec = provider.embed_query("hello world")
    assert isinstance(vec, list)
    assert all(isinstance(x, float) for x in vec)


def test_huggingface_embed_documents():
    provider = HuggingFaceEmbeddingProvider("all-MiniLM-L6-v2")
    vecs = provider.embed_documents(["hello", "world"])
    assert len(vecs) == 2
    assert len(vecs[0]) > 0


def test_embeddings_are_deterministic():
    provider = HuggingFaceEmbeddingProvider("all-MiniLM-L6-v2")
    v1 = provider.embed_query("test sentence")
    v2 = provider.embed_query("test sentence")
    assert v1 == v2
