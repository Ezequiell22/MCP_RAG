import re
from pathlib import Path

import yaml


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
    sections = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
    return sections


def load_guide(path: Path, guides_dir: Path | None = None) -> dict:
    content = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)
    sections = extract_sections(body)
    rel_path = path.relative_to(guides_dir) if guides_dir else path
    return {
        "path": str(rel_path),
        "filename": path.name,
        "descricao": meta.get("descricao", ""),
        "palavras_chave": meta.get("palavras_chave", []),
        "content": body,
        "secoes": sections,
    }
