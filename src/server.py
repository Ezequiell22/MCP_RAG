import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP

from src.application.document_service import DocumentService
from src.application.indexing_service import IndexingService
from src.application.search_service import SearchService
from src.config.logging import setup_logging
from src.config.settings import load_settings

log = setup_logging()

_search_service: SearchService | None = None
_document_service: DocumentService | None = None
_indexing_service: IndexingService | None = None

mcp = FastMCP("mcp-documentacao")


@mcp.tool()
async def buscar_documentacao(pergunta: str, limite: int = 5) -> list[dict]:
    """Busca trechos relevantes de documentação para a pergunta."""
    return [r.model_dump() for r in _search_service.search(pergunta, k=limite)]


@mcp.tool()
async def listar_guias() -> list[dict]:
    """Lista todos os guias disponíveis com descrição, palavras-chave e seções."""
    return [g.model_dump() for g in _document_service.list_guides()]


@mcp.tool()
async def reindexar() -> str:
    """Força a reindexação completa de todos os guias."""
    _search_service.clear_cache()
    _indexing_service.index_all()
    return "Reindexação concluída."


def main():
    global _search_service, _document_service, _indexing_service

    config_path = os.environ.get("CONFIG_PATH", "config.yaml")
    settings = load_settings(config_path)

    indexing_service = IndexingService(settings)
    indexing_service.set_logger(log)

    document_service = DocumentService(settings)

    log.info("Starting MCP Documentação...")
    log.info("Guides dir: %s", settings.guides_dir)
    log.info("Embedding: %s / %s", settings.embedding.provider, settings.embedding.model)

    indexing_service.index_all()

    search_service = SearchService(
        settings,
        vector_store=indexing_service.vector_store,
        bm25=indexing_service.bm25,
        embedding_provider=indexing_service.embedding_provider,
    )
    search_service.set_logger(log)

    _search_service = search_service
    _document_service = document_service
    _indexing_service = indexing_service

    log.info("MCP ready on stdio")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
