from sentence_transformers import SentenceTransformer
from app.config import get_settings
from functools import lru_cache
from typing import List

settings = get_settings()


@lru_cache
def get_embedder() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model, device="cpu")


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedder()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
        batch_size=32
    )
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    return embed_texts([query])[0]