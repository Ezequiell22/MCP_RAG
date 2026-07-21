O MCP deveria fazer apenas recuperação de informação (retrieval), não geração. Ficaria assim:

Agente
    │
    ▼
MCP
    │
    ├── BM25
    ├── Embeddings
    ├── Chroma
    └── Markdown

O fluxo seria:

O agente pergunta:

Como registrar um componente Delphi?
O MCP gera o embedding da pergunta (modelo de embeddings, não um LLM).
Pesquisa no Chroma.
Retorna os 5 melhores chunks.
O LLM do agente lê esses chunks e responde.

Ou seja:

LLM
   │
   ▼
MCP
   │
Embedding Model
   │
Vector DB

Não existe um segundo LLM.

Embeddings ≠ LLM

Muita gente confunde.

Um modelo de embeddings apenas transforma texto em um vetor.

"Como criar um componente"

↓

[0.12, -0.44, 0.91, ...]

Ele não escreve texto.

Não faz raciocínio.

Não responde perguntas.

Só gera uma representação numérica.

É extremamente barato.

Inclusive pode ser local

Você pode usar, por exemplo:

bge-small
bge-base
jina-embeddings-v3
nomic-embed-text
all-MiniLM-L6-v2

Todos rodam localmente.

Sem custo de API.

Eu faria ainda mais simples

Como seus documentos são Markdown, eu faria o índice apenas quando o MCP inicia.

docs/

acbr.md
delphi.md
movidesk.md
sql.md
...

Ao iniciar:

Markdown
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
Chroma

Isso acontece uma única vez.

Depois toda chamada é apenas:

buscar_documentacao(
    pergunta="Como criar um componente Delphi?"
)

retornando algo como:

[
  {
    "arquivo": "delphi/componentes.md",
    "titulo": "Criando Componentes",
    "score": 0.94,
    "conteudo": "..."
  }
]
Como eu faria no seu caso

Conhecendo a arquitetura que você já está construindo (LangGraph + MCP para documentação + agentes especializados), eu nem chamaria a ferramenta de obter_bundle.

Criaria algo como:

buscar_documentacao(
    pergunta: str,
    limite: int = 5
)

E internamente ela faria:

Pergunta
    │
    ▼
Embedding
    │
    ▼
Busca vetorial + BM25
    │
    ▼
Top 5 chunks

O agente receberia apenas cerca de 500–1500 tokens em vez de um documento inteiro com 10–20 mil tokens. Isso reduz custo, melhora a qualidade do contexto e escala muito melhor conforme seu repositório cresce.

Descreva como seria o desenvolvimento desse mcp, com python, langchain, bons padroes de codigo, chromadb talvez?

Eu seguiria uma arquitetura bem parecida com a de um RAG, mas encapsulada em um MCP. A diferença é que o MCP não gera respostas: ele apenas indexa, busca e devolve os trechos mais relevantes para o agente.

Arquitetura
                   ┌────────────────────────┐
                   │  Repositório Guides    │
                   │      *.md              │
                   └────────────┬───────────┘
                                │
                    Indexação (startup ou comando)
                                │
                                ▼
                     Markdown Loader
                                │
                                ▼
                    Document Splitter
                                │
                                ▼
                  Geração de Embeddings
                                │
                                ▼
                          ChromaDB
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
     Busca Vetorial                      Busca BM25
             │                                     │
             └──────────────────┬──────────────────┘
                                │
                           Merge + Ranking
                                │
                                ▼
                      Resposta do MCP
Estrutura do projeto

Eu organizaria o código em camadas, evitando colocar toda a lógica dentro do servidor MCP.

src/
│
├── server.py
│
├── config/
│   ├── settings.py
│   └── logging.py
│
├── application/
│   ├── indexing_service.py
│   ├── search_service.py
│   └── document_service.py
│
├── domain/
│   ├── models.py
│   └── interfaces.py
│
├── infrastructure/
│   ├── chromadb_repository.py
│   ├── embedding_provider.py
│   ├── markdown_loader.py
│   ├── splitter.py
│   └── bm25_repository.py
│
├── tools/
│   ├── search_documentation.py
│   ├── list_guides.py
│   └── rebuild_index.py
│
└── guides/

Essa separação facilita testes e permite trocar o Chroma por outro banco vetorial no futuro.

Stack

Eu utilizaria:

Python 3.12+
LangChain
ChromaDB
FastMCP
Pydantic
Markdown
rank-bm25
uv

Nada de banco SQL.

O próprio Chroma persiste os dados.

Processo de indexação

Quando o MCP iniciar:

guia.md

↓

MarkdownLoader

↓

Document

↓

Chunking

↓

Embeddings

↓

Chroma

Cada chunk possuiria metadados.

Exemplo:

{
    "guide": "delphi",
    "section": "Componentes",
    "path": "delphi/componentes.md",
    "tags": [
        "vcl",
        "component"
    ]
}

Esses metadados ajudam muito na filtragem.

Chunking

Não usaria o splitter padrão.

Criaria um splitter específico para Markdown.

Exemplo:

# Componentes

texto...

## Registro

texto...

### Exemplo

texto...

Cada seção vira um chunk.

Nunca cortar no meio de um tópico.

O agente entende muito melhor.

Embeddings

Eu deixaria uma interface.

class EmbeddingProvider(ABC):

    @abstractmethod
    def embed_documents(...):
        ...

    @abstractmethod
    def embed_query(...):
        ...

Implementações:

OpenAIEmbeddingProvider

JinaEmbeddingProvider

BGEEmbeddingProvider

OllamaEmbeddingProvider

Troca apenas por configuração.

Chroma

Cada chunk seria armazenado como

id

conteudo

embedding

metadata

Nada além disso.

Busca

A ferramenta do MCP seria algo como

buscar_documentacao(
    pergunta,
    limite=5
)

Internamente

pergunta

↓

embedding

↓

Chroma.similarity_search()

↓

5 chunks
Busca híbrida

Depois de algum tempo eu adicionaria BM25.

Fluxo

pergunta

↓

BM25

↓

Vetorial

↓

Merge

↓

Ranking

Isso resolve buscas como

ACBrNFeMonitorPLUS

que embeddings nem sempre encontram bem.

Ferramentas MCP

Hoje você possui

obter_bundle()

Eu substituiria por

buscar_documentacao()

listar_guias()

listar_topicos()

buscar_por_guia()

reindexar()

Exemplo

buscar_documentacao(
    pergunta="Como registrar um componente Delphi?",
    guia="Delphi",
    limite=5
)
Reindexação

Não faria embeddings toda vez que inicia.

Criaria um hash.

guia.md

↓

SHA256

↓

Mudou?

↓

Sim

↓

Reindexa

↓

Não

↓

Ignora

Em um repositório com centenas de arquivos isso faz muita diferença.

Cache

Também faria cache das consultas.

Como registrar componente?

↓

hash

↓

Existe?

↓

Sim

↓

Retorna imediatamente

Pode reduzir bastante chamadas repetidas.

Testes

Separaria em:

tests/

test_splitter.py

test_loader.py

test_indexer.py

test_search.py

test_embeddings.py

Cada camada testada isoladamente.

Configuração

Tudo via YAML.

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

Nada hardcoded.

Logging

Logs estruturados.

INFO

Loading guides...

Indexed 542 chunks

Embedding completed

Search:

Query:
"Como criar componente"

Returned:
5 chunks

Latency:
74 ms

Facilita monitorar desempenho e diagnosticar problemas.

Evolução futura

Depois dessa base pronta, há algumas evoluções que agregam bastante valor sem aumentar muito a complexidade:

Busca híbrida com reranking: combinar BM25 + busca vetorial e usar um reranker (como BGE Reranker ou Jina Reranker) para reordenar os resultados antes de devolvê-los ao agente.
Índice hierárquico: permitir listar guias, seções e subseções antes de abrir conteúdo, reduzindo ainda mais o contexto enviado ao LLM.
Watcher de arquivos: monitorar alterações na pasta guides/ e reindexar apenas os arquivos modificados.
Versionamento do índice: associar cada índice a uma versão ou commit do repositório de documentação, facilitando auditoria e rollback.
Filtros por metadados: restringir buscas por guia, linguagem, módulo ou tags (Delphi, SQL, ACBr, Movidesk, etc.).
Métricas: expor tempo de indexação, tempo médio de busca, quantidade de chunks e taxa de acerto das consultas.

Esse desenho mantém o MCP responsável apenas pela recuperação eficiente de conhecimento, enquanto o agente continua sendo o único componente que utiliza um LLM para interpretar os trechos recuperados e gerar a resposta final. É uma separação de responsabilidades que tende a escalar bem e facilita a manutenção do projeto.