import time
import requests

from app.core.settings import settings


def create_jina_embedding(text: str) -> list[float]:
    if not settings.JINA_API_KEY:
        raise ValueError("JINA_API_KEY is not configured")

    last_error = None

    for attempt in range(3):
        try:
            response = requests.post(
                settings.JINA_BASE_URL,
                headers={
                    "Authorization": f"Bearer {settings.JINA_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.JINA_EMBEDDING_MODEL,
                    "input": [text],
                },
                timeout=120,
            )

            if not response.ok:
                raise RuntimeError(
                    f"Jina embedding failed: "
                    f"{response.status_code} {response.text}"
                )

            data = response.json()

            return data["data"][0]["embedding"]

        except Exception as error:
            last_error = error
            time.sleep(2 * (attempt + 1))

    raise RuntimeError(
        f"Jina embedding failed after retries: {last_error}"
    )


def create_jina_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
     
    if not settings.JINA_API_KEY:
        raise ValueError("JINA_API_KEY is not configured")

    response = requests.post(
        settings.JINA_BASE_URL,
        headers={
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.JINA_EMBEDDING_MODEL,
            "input": texts,
        },
        timeout=300,
    )

    if not response.ok:
        raise RuntimeError(
            f"Jina embedding failed: {response.status_code} {response.text}"
        )

    data = response.json()

    return [
        item["embedding"]
        for item in data["data"]
    ]