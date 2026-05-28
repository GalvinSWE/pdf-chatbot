from openai import OpenAI

from app.core.settings import settings

client = OpenAI(
    base_url=settings.OPENROUTER_BASE_URL,
    api_key=settings.OPENROUTER_API_KEY,
)

def create_chat_response(message: str) -> str:
    response = client.chat.completions.create(
        model=settings.OPENROUTER_MODEL,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    return response.choices[0].message.content