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
async def buscar_documentacao(pergunta: str, limite: int = 5, fonte: str | None = None) -> list[dict]:
    """Busca trechos relevantes de documentação. Use 'fonte' para filtrar por tipo (ex: documento, guia, faq)."""
    return [r.model_dump() for r in _search_service.search(pergunta, k=limite, fonte=fonte)]


@mcp.tool()
async def listar_documentos() -> list[dict]:
    """Lista todos os documentos disponíveis com descrição, palavras-chave, seções e fonte."""
    return [g.model_dump() for g in _document_service.list_documents()]


@mcp.tool()
async def reindexar() -> str:
    """Força a reindexação completa de todas as fontes de documentos."""
    _search_service.clear_cache()
    _indexing_service.index_all()
    return "Reindexação concluída."


def _start_watcher(indexing_service: IndexingService, search_service: SearchService):
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class ReindexHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path.endswith((".md", ".txt")):
                    log.info("File change detected: %s", event.src_path)
                    search_service.clear_cache()
                    indexing_service.index_all()

            def on_created(self, event):
                self.on_modified(event)

        observer = Observer()
        for source in indexing_service.settings.resolve_sources():
            p = Path(source.path)
            if p.exists():
                observer.schedule(ReindexHandler(), str(p), recursive=True)
                log.info("Watching: %s", p)
        observer.start()
        return observer
    except ImportError:
        log.info("watchdog not installed, file watcher disabled")
        return None


def main():
    global _search_service, _document_service, _indexing_service

    config_path = os.environ.get("CONFIG_PATH", "config.yaml")
    settings = load_settings(config_path)

    indexing_service = IndexingService(settings)
    indexing_service.set_logger(log)

    document_service = DocumentService(settings)

    log.info("Starting MCP Documentação...")
    for s in settings.resolve_sources():
        log.info("  Source: %s [%s] -> %s", s.path, s.type, s.description or "(sem descrição)")
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

    _start_watcher(indexing_service, search_service)

    log.info("MCP ready on stdio")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
