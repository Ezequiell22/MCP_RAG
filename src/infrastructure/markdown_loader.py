import re
from pathlib import Path

import yaml

from src.domain.interfaces import DocumentLoader


def parse_frontmatter(content: str) -> tuple[dict, str]:
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                meta = {}
            body = parts[2]
            return meta, body
    return {}, content


def extract_sections(content: str) -> list[str]:
    return re.findall(r"^##\s+(.+)$", content, re.MULTILINE)


class MarkdownLoader(DocumentLoader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".md"

    def load(self, path: Path, source_dir: Path | None = None, source_type: str = "documento") -> dict:
        content = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        sections = extract_sections(body)
        rel_path = path.relative_to(source_dir) if source_dir else path
        return {
            "path": str(rel_path),
            "filename": path.name,
            "descricao": meta.get("descricao", ""),
            "palavras_chave": meta.get("palavras_chave", []),
            "content": body,
            "secoes": sections,
            "fonte": source_type,
        }
