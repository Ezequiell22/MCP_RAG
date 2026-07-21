from pathlib import Path

from src.config.settings import Settings
from src.domain.models import DocumentInfo
from src.infrastructure.markdown_loader import load_document


class DocumentService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def list_documents(self) -> list[DocumentInfo]:
        result: list[DocumentInfo] = []
        for source in self.settings.resolve_sources():
            source_dir = Path(source.path)
            if not source_dir.exists():
                continue
            for md_path in sorted(source_dir.rglob("*.md")):
                try:
                    doc = load_document(md_path, source_dir, source.type)
                except Exception:
                    continue
                result.append(DocumentInfo(
                    arquivo=doc["path"],
                    descricao=doc["descricao"],
                    palavras_chave=doc["palavras_chave"],
                    secoes=doc["secoes"],
                    fonte=doc["fonte"],
                ))
        return result
