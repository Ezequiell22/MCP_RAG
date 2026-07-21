import re

from src.config.settings import ChunkingConfig
from src.domain.models import Chunk


def split_markdown(text: str, path: str, metadata: dict, config: ChunkingConfig) -> list[Chunk]:
    chunks: list[Chunk] = []
    lines = text.split("\n")
    current_section = "Introdução"
    current_lines: list[str] = []
    chunk_index = 0

    def flush():
        nonlocal chunk_index
        content = "\n".join(current_lines).strip()
        if content:
            chunk_meta = {**metadata, "section": current_section}
            chunks.append(Chunk(
                id=f"{path}#{chunk_index}",
                content=content,
                metadata=chunk_meta,
            ))
            chunk_index += 1

    for line in lines:
        if re.match(r"^#{2,4} ", line):
            flush()
            current_section = re.sub(r"^#+\s*", "", line).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    flush()
    return chunks
