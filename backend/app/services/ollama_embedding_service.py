import requests

from app.core.settings import settings

def create_embedding(text: str) -> list[float]:
    url = f"{settings.OLLAMA_BASE_URL}/api/embeddings"

    response = requests.post(
        url,
        json={
            "model": settings.OLLAMA_EMBEDDING_MODEL,
            "prompt": text,
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]