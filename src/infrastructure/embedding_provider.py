from src.domain.interfaces import EmbeddingProvider


class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text, show_progress_bar=False).tolist()


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model_name = model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI()
        return self._client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        resp = self.client.embeddings.create(input=texts, model=self.model_name)
        return [r.embedding for r in resp.data]

    def embed_query(self, text: str) -> list[float]:
        resp = self.client.embeddings.create(input=[text], model=self.model_name)
        return resp.data[0].embedding


class JinaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str = "jina-embeddings-v3", api_key: str | None = None):
        self.model_name = model
        self.api_key = api_key
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text, show_progress_bar=False).tolist()


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.model_name = model
        self.base_url = base_url
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import ollama
            self._client = ollama.Client(host=self.base_url)
        return self._client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.client.embeddings(model=self.model_name, prompt=t)["embedding"] for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.client.embeddings(model=self.model_name, prompt=text)["embedding"]
