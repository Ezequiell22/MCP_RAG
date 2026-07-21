from pathlib import Path

import yaml
from pydantic import BaseModel


class EmbeddingConfig(BaseModel):
    provider: str = "huggingface"
    model: str = "paraphrase-multilingual-MiniLM-L12-v2"


class SearchConfig(BaseModel):
    top_k: int = 5
    hybrid: bool = True
    cache_max_size: int = 200
    cache_ttl: int = 3600


class ChunkingConfig(BaseModel):
    max_size: int = 1000
    overlap: int = 200


class SourceConfig(BaseModel):
    path: Path
    type: str = "documento"
    description: str = ""


class Settings(BaseModel):
    sources: list[SourceConfig] = []
    db_path: Path = Path("./chroma_db")
    collection_name: str = "documents"
    embedding: EmbeddingConfig = EmbeddingConfig()
    search: SearchConfig = SearchConfig()
    chunking: ChunkingConfig = ChunkingConfig()

    def resolve_sources(self) -> list[SourceConfig]:
        return self.sources


def load_settings(path: str | None = None) -> Settings:
    path = path or Path.cwd() / "config.yaml"
    if not Path(path).exists():
        return Settings()

    with open(path) as f:
        data = yaml.safe_load(f) or {}

    sources_data = data.pop("sources", None)
    guides_dir = data.pop("guides_dir", None)

    settings = Settings(**data)

    if sources_data:
        settings.sources = [SourceConfig(**s) for s in sources_data]
    elif guides_dir:
        settings.sources = [SourceConfig(path=Path(guides_dir), type="documento", description="Documentos")]

    return settings
