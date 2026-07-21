import re

from src.config.settings import ChunkingConfig
from src.domain.models import Chunk


def _split_long_text(text: str, config: ChunkingConfig) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len <= config.max_size:
            current.append(para)
            current_len += para_len
        else:
            if current:
                chunks.append("\n\n".join(current))
            if para_len > config.max_size:
                for i in range(0, len(para), config.max_size - config.overlap):
                    chunks.append(para[i:i + config.max_size])
            else:
                current = [para]
                current_len = para_len

    if current:
        chunks.append("\n\n".join(current))
    return chunks


def split_markdown(text: str, path: str, metadata: dict, config: ChunkingConfig) -> list[Chunk]:
    chunks: list[Chunk] = []
    lines = text.split("\n")
    current_section = "Introdução"
    current_lines: list[str] = []
    chunk_index = 0

    def flush():
        nonlocal chunk_index
        content = "\n".join(current_lines).strip()
        if not content:
            return

        chunk_meta = {**metadata, "section": current_section}

        if len(content) <= config.max_size:
            chunks.append(Chunk(
                id=f"{path}#{chunk_index}",
                content=content,
                metadata=chunk_meta,
            ))
            chunk_index += 1
        else:
            for part in _split_long_text(content, config):
                chunks.append(Chunk(
                    id=f"{path}#{chunk_index}",
                    content=part,
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
