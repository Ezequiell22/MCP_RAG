from pathlib import Path

from src.config.settings import Settings
from src.domain.models import GuiaInfo
from src.infrastructure.markdown_loader import load_guide


class DocumentService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def list_guides(self) -> list[GuiaInfo]:
        guides_dir = Path(self.settings.guides_dir)
        if not guides_dir.exists():
            return []
        result: list[GuiaInfo] = []
        for md_path in sorted(guides_dir.rglob("*.md")):
            try:
                guide = load_guide(md_path)
            except Exception:
                continue
            result.append(GuiaInfo(
                arquivo=guide["path"],
                descricao=guide["descricao"],
                palavras_chave=guide["palavras_chave"],
                secoes=guide["secoes"],
            ))
        return result
