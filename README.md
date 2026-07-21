# mcp-documentacao

MCP server que indexa documentos técnicos e disponibiliza busca via RAG híbrida (vetorial + BM25). Apenas recuperação — sem geração.

## Uso

```bash
pip install .
python3 src/server.py
```

O servidor roda via stdio — compatível com qualquer cliente MCP.

## Configuração

Edite `config.yaml`:

```yaml
sources:
  - path: ./src/guides
    type: documento
    description: Documentos técnicos

db_path: ./chroma_db
collection_name: documents

embedding:
    provider: huggingface   # huggingface | openai | jina | ollama
    model: paraphrase-multilingual-MiniLM-L12-v2

search:
    top_k: 5
    hybrid: true
    cache_max_size: 200
    cache_ttl: 3600

chunking:
    max_size: 1000
    overlap: 200
```

`CONFIG_PATH` pode ser passada como variável de ambiente.

## Ferramentas MCP

| Ferramenta | Descrição |
|---|---|
| `buscar_documentacao(pergunta, limite?, fonte?)` | Busca trechos relevantes |
| `listar_documentos()` | Lista documentos indexados |
| `reindexar()` | Reindexa todas as fontes |

O parâmetro `fonte` filtra por tipo de fonte (ex: `documento`, `faq`).

## Fontes

Múltiplas fontes com tipos arbitrários. Formatos suportados: Markdown (`.md`) e texto (`.txt`). Frontmatter YAML é lido como metadados (descrição, palavras-chave).

## Docker

```bash
docker compose up --build
```

Monte volumes para `/app/src/guides` e `/app/chroma_db` para persistência.

## Testes

```bash
pip install pytest
pytest tests/
```

## Provedores de embedding

- **huggingface** (padrão, local) — `all-MiniLM-L6-v2`, `paraphrase-multilingual-MiniLM-L12-v2`
- **openai** — `text-embedding-3-small`, `text-embedding-3-large` (requer `OPENAI_API_KEY`)
- **jina** — `jina-embeddings-v3` (requer `JINA_API_KEY`)
- **ollama** — modelos locais via Ollama
