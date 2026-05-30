from app.core.settings import settings
from app.services.jina_embedding_service import (
    create_jina_embedding,
    create_jina_embeddings,
)
from app.services.ollama_embedding_service import (
    create_embedding as create_ollama_embedding,
)

def create_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Cannot create embedding for empty text")

    if settings.EMBEDDING_PROVIDER == "jina":
        return create_jina_embedding(text)

    if settings.EMBEDDING_PROVIDER == "ollama":
        return create_ollama_embedding(text)

    raise ValueError(
        f"Unsupported EMBEDDING_PROVIDER: {settings.EMBEDDING_PROVIDER}"
    )


def create_embeddings(texts: list[str]) -> list[list[float]]:
    cleaned_texts = [
        text.strip()
        for text in texts
        if text and text.strip()
    ]

    if not cleaned_texts:
        return []

    if settings.EMBEDDING_PROVIDER == "jina":
        return create_jina_embeddings(cleaned_texts)

    if settings.EMBEDDING_PROVIDER == "ollama":
        return [
            create_ollama_embedding(text)
            for text in cleaned_texts
        ]

    raise ValueError(
        f"Unsupported EMBEDDING_PROVIDER: {settings.EMBEDDING_PROVIDER}"
    )