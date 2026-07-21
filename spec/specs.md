# Specs — MCP de Documentação (RAG Puro)

> **Princípio fundamental**: O MCP faz apenas **recuperação** (retrieval). Nunca geração.
> O agente (LLM) é o único que interpreta os trechos e gera a resposta final.

---

## 1. Stack

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12+ | Runtime |
| FastMCP | — | Framework MCP |
| LangChain | — | Loaders, splitters, embeddings |
| ChromaDB | — | Vector store |
| rank-bm25 | — | Busca lexical |
| Pydantic | — | Schemas e validação |
| PyYAML | — | Config |
| uv | — | Gerenciamento de dependências |

Nada de banco SQL. O Chroma persiste os dados por conta própria.

---

## 2. Estrutura do Projeto

```
src/
├── server.py                  # Servidor MCP (FastMCP)
├── config/
│   ├── settings.py            # Leitura do YAML
│   └── logging.py             # Logs estruturados
├── application/
│   ├── indexing_service.py    # Orquestração da indexação
│   ├── search_service.py      # Orquestração da busca
│   └── document_service.py    # Operações sobre documentos
├── domain/
│   ├── models.py              # Entidades (Chunk, Guia, etc.)
│   └── interfaces.py          # Contratos/ABCs
├── infrastructure/
│   ├── chromadb_repository.py # Acesso ao Chroma
│   ├── embedding_provider.py  # Interface + impls de embeddings
│   ├── markdown_loader.py     # Loader customizado
│   ├── splitter.py            # Splitter específico para Markdown
│   └── bm25_repository.py     # Índice BM25
├── tools/
│   ├── search_documentation.py
│   ├── list_guides.py
│   └── rebuild_index.py
├── tests/
│   ├── test_splitter.py
│   ├── test_loader.py
│   ├── test_indexer.py
│   ├── test_search.py
│   └── test_embeddings.py
└── guides/                    # Documentos fonte (.md)
```

---

## 3. Ferramentas MCP

Apenas duas ferramentas de busca + uma de manutenção.

### 3.1 `buscar_documentacao`

Ferramenta principal. O agente faz perguntas em linguagem natural.

```python
buscar_documentacao(
    pergunta: str,
    limite: int = 5,
) -> list[ChunkResult]
```

Fluxo interno:
1. Gera embedding da pergunta (modelo de embeddings, não LLM)
2. Busca vetorial no Chroma (similarity_search)
3. (Opcional) Busca BM25 paralela
4. Merge + ranking dos resultados
5. Retorna top-K chunks com: arquivo, título, score, conteúdo

Não precisa de filtro por guia — o embedding + BM25 já trazem os chunks certos.

### 3.2 `listar_guias`

Retorna o catálogo de documentos disponíveis. Útil para o agente saber o que existe.

```python
listar_guias() -> list[GuiaInfo]
```

Onde `GuiaInfo` contém:

| Campo | Descrição |
|---|---|
| `arquivo` | Nome do arquivo (ex: `delphi/componentes.md`) |
| `descricao` | Breve descrição do guia |
| `palavras_chave` | ~5 palavras-chave (ex: `["delphi", "vcl", "componente", "registro"]`) |
| `secoes` | Lista de seções principais (`##`) |

Descrição e palavras-chave vêm do frontmatter YAML de cada `.md`.

O agente pode chamar `listar_guias()` para decidir o que perguntar, ou ir direto em `buscar_documentacao`.

### 3.3 `reindexar`

Força a reindexação de todos os guias.

---

## 4. Indexação

### 4.1 Fluxo (executado na inicialização ou sob demanda)

```
guia.md
    ↓
MarkdownLoader
    ↓
Document (metadados: guide, section, path, descricao, palavras_chave)
    ↓
MarkdownSplitter (custom — chunk por seção ##)
    ↓
Geração de embeddings
    ↓
ChromaDB (id, conteudo, embedding, metadata)
    ↓
BM25 index
```

### 4.2 Splitter customizado para Markdown

- Divide por seções (`##`, `###`, etc.)
- Cada seção vira um chunk completo
- **Nunca** corta no meio de um tópico
- Metadados preservam: `guide`, `section`, `path`, `tags`

### 4.3 Metadados

**Por arquivo** (frontmatter YAML):

```yaml
---
descricao: "Guia completo sobre criação de componentes Delphi"
palavras_chave: [delphi, vcl, componente, registro, pacote]
---
```

**Por chunk** (gerado automaticamente):

```json
{
    "guide": "delphi",
    "section": "Componentes",
    "path": "delphi/componentes.md",
    "descricao": "Guia completo sobre criação de componentes Delphi",
    "palavras_chave": ["delphi", "vcl", "componente", "registro", "pacote"]
}
```

Descrição e palavras-chave são herdadas do arquivo para todos os chunks.

---

## 5. Embeddings

### 5.1 Interface

```python
class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    @abstractmethod
    def embed_query(self, text: str) -> list[float]: ...
```

### 5.2 Implementações

| Provedor | Modelo sugerido | Local? |
|---|---|---|
| `OpenAIEmbeddingProvider` | text-embedding-3-small | Não |
| `JinaEmbeddingProvider` | jina-embeddings-v3 | Sim |
| `BGEEmbeddingProvider` | bge-small / bge-base | Sim |
| `OllamaEmbeddingProvider` | nomic-embed-text | Sim |
| `HuggingFaceEmbeddingProvider` | all-MiniLM-L6-v2 | Sim |

Troca apenas por configuração. Preferência por modelos locais.

Embeddings ≠ LLM — não geram texto, não raciocinam, apenas produzem vetores. Extremamente baratos.

---

## 6. Busca Híbrida

### 6.1 Fluxo

```
pergunta
    ↓
Embedding ──► Chroma (similarity_search)
    ↓
BM25 ──► rank_bm25
    ↓
Merge + Ranking (combinação linear ou RRF)
    ↓
Top-K chunks
```

A busca híbrida resolve consultas com termos exatos (ex: `ACBrNFeMonitorPLUS`) que embeddings isoladamente perderiam.

### 6.2 Cache de consultas

```python
cache: dict[str, list[ChunkResult]]  # hash da pergunta → resultado
```

Reduz chamadas repetidas ao embedding + vector DB.

---

## 7. Reindexação Inteligente

- Cada arquivo tem hash SHA256 armazenado
- Na inicialização, compara hash atual com o anterior
- Só reindexa se o arquivo mudou
- Economia significativa em repositórios com centenas de arquivos

---

## 8. Configuração (YAML)

```yaml
embedding:
    provider: jina
    model: jina-embeddings-v3

vectorstore:
    provider: chroma
    persist_directory: ./db

chunking:
    size: 1000
    overlap: 200

search:
    top_k: 5
    hybrid: true
```

Nada hardcoded.

---

## 9. Logging

Logs estruturados com níveis:

```
INFO  — Loading guides...
INFO  — Indexed 542 chunks
INFO  — Embedding completed
INFO  — Query: "Como criar componente" | Returned: 5 chunks | Latency: 74 ms
ERROR — Failed to load guide: delphi/erro.md
```

Facilita monitoramento de desempenho e diagnóstico.

---

## 10. Resposta do MCP

```json
[
    {
        "arquivo": "delphi/componentes.md",
        "titulo": "Criando Componentes",
        "score": 0.94,
        "conteudo": "Para criar um componente Delphi..."
    }
]
```

O agente recebe ~500–1500 tokens em vez de documentos inteiros de 10–20 mil tokens.

---

## 11. Testes

| Teste | O que valida |
|---|---|
| `test_splitter.py` | Chunking correto de seções markdown |
| `test_loader.py` | Loader lê metadados corretamente |
| `test_indexer.py` | Indexação e reindexação com hash |
| `test_search.py` | Busca vetorial, BM25, híbrida |
| `test_embeddings.py` | Interface de embedding e provedores |

Cada camada testada isoladamente.

---

## 13. Decisões de Implementação

### 13.1 Modelos (Pydantic)

```python
class ChunkResult(BaseModel):
    arquivo: str       # path relativo (ex: delphi/componentes.md)
    titulo: str        # nome da seção (##)
    score: float       # relevância (0-1)
    conteudo: str      # texto do chunk

class GuiaInfo(BaseModel):
    arquivo: str
    descricao: str
    palavras_chave: list[str]
    secoes: list[str]  # títulos das seções (##) no documento
```

### 13.2 Config

- Arquivo: `config.yaml` na raiz do projeto
- Override via env var `CONFIG_PATH`
- Tudo resolvido via Pydantic `BaseModel` com defaults sensíveis

### 13.3 Chroma

- Collection name: `"guides"` (fixo)
- Espaço de similaridade: cosseno
- Persistência no diretório definido em `db_path`

### 13.4 Embedding default

- Provider: `huggingface` (sentence-transformers)
- Modelo: `all-MiniLM-L6-v2`
- Download automático na primeira execução
- Sem necessidade de API key para o default

### 13.5 Frontmatter

- Parseado com `yaml.safe_load` após split por `---`
- Sem dependência extra (PyYAML já está na stack)
- Se frontmatter inválido, loga WARNING e continua com metadados vazios
- Se não tiver frontmatter, metadados vazios — não quebra

### 13.6 Erros

- Chroma vazio → `buscar_documentacao` retorna lista vazia, nunca exception
- Arquivo corrompido → log ERROR, pula, não interrompe indexação
- Provider de embedding falhou → exception propaga (não tem fallback sensível)

### 13.7 Dependências (pyproject.toml)

```toml
dependencies = [
    "mcp>=1.0.0",
    "chromadb>=0.5.0",
    "sentence-transformers>=3.0.0",
    "rank-bm25>=0.2.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0",
]
```

### 13.8 Como rodar

```bash
pip install uv && uv sync
python src/server.py
# ou
uv run python src/server.py
```

O MCP se comunica via **stdio** — o agente (LangGraph) o invoca como subprocesso.

---

## 14. Evoluções Futuras

1. **Reranking**: BGE Reranker / Jina Reranker após busca híbrida
2. **Índice hierárquico**: guias → seções → subseções
3. **Watcher de arquivos**: reindexação automática ao modificar `guides/`
4. **Versionamento**: associar índice a commit/versão da doc
5. **Filtros avançados**: por guia, linguagem, módulo, tags
6. **Métricas**: tempo de indexação, busca, taxa de acerto
