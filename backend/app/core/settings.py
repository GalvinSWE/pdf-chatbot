from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "openrouter/free"

    EMBEDDING_PROVIDER: str = "jina"
    JINA_API_KEY: str | None = None
    JINA_BASE_URL: str = "https://api.jina.ai/v1/embeddings"
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v3"
    JINA_EMBEDDING_DIMENSION: int = 1024

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
    )


settings = Settings()