from openai import OpenAI
from app.core.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def create_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding

def create_chat_response(message: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=message,
    )

    return response.output_text