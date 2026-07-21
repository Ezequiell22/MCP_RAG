import chromadb
from chromadb.config import Settings as ChromaSettings

from src.domain.interfaces import VectorStore
from src.domain.models import Chunk, ChunkResult


class ChromaRepository(VectorStore):
    def __init__(self, db_path: str, collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[c.metadata for c in chunks],
            embeddings=embeddings,
        )

    def similarity_search(self, query_embedding: list[float], k: int = 5, where: dict | None = None) -> list[ChunkResult]:
        if self.collection.count() == 0:
            return []
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"],
            where=where,
        )
        output: list[ChunkResult] = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i] or {}
            distance = results["distances"][0][i]
            output.append(ChunkResult(
                id=results["ids"][0][i],
                arquivo=meta.get("path", ""),
                titulo=meta.get("section", ""),
                score=1.0 - distance,
                conteudo=results["documents"][0][i],
                fonte=meta.get("fonte", ""),
            ))
        return output

    def count(self) -> int:
        return self.collection.count()

    def delete_all(self) -> None:
        name = self.collection.name
        self.client.delete_collection(name)
        self.collection = self.client.create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
