from pathlib import Path

from src.domain.interfaces import DocumentLoader


class TextLoader(DocumentLoader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in (".txt", ".text")

    def load(self, path: Path, source_dir: Path | None = None, source_type: str = "documento") -> dict:
        content = path.read_text(encoding="utf-8")
        rel_path = path.relative_to(source_dir) if source_dir else path
        return {
            "path": str(rel_path),
            "filename": path.name,
            "descricao": "",
            "palavras_chave": [],
            "content": content,
            "secoes": [],
            "fonte": source_type,
        }
