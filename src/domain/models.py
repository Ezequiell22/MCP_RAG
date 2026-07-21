from pydantic import BaseModel


class ChunkResult(BaseModel):
    id: str = ""
    arquivo: str
    titulo: str
    score: float
    conteudo: str


class GuiaInfo(BaseModel):
    arquivo: str
    descricao: str
    palavras_chave: list[str]
    secoes: list[str]


class Chunk(BaseModel):
    id: str
    content: str
    metadata: dict


class IndexedChunk(Chunk):
    embedding: list[float]
