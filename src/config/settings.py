from pathlib import Path

import yaml
from pydantic import BaseModel


class EmbeddingConfig(BaseModel):
    provider: str = "huggingface"
    model: str = "all-MiniLM-L6-v2"


class SearchConfig(BaseModel):
    top_k: int = 5
    hybrid: bool = True


class ChunkingConfig(BaseModel):
    max_size: int = 1000
    overlap: int = 200


class Settings(BaseModel):
    guides_dir: Path = Path("./src/guides")
    db_path: Path = Path("./chroma_db")
    embedding: EmbeddingConfig = EmbeddingConfig()
    search: SearchConfig = SearchConfig()
    chunking: ChunkingConfig = ChunkingConfig()


def load_settings(path: str | None = None) -> Settings:
    path = path or Path.cwd() / "config.yaml"
    if not Path(path).exists():
        return Settings()
    with open(path) as f:
        data = yaml.safe_load(f)
    return Settings(**data)
