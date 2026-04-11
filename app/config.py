from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API ключи
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    DART_API_KEY: str  # DART Open API key for Korean corporate disclosures (dart.fss.or.kr)

    # LLM settings
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1000

    # База данных
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    # App / JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    APP_ENV: Literal["development", "production", "test"] = "development"  # Application environment

    # LLM
    LLM_MODEL: str = 'llama-3.3-70b-versatile'

    # Log
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # MCP Server
    TAVILY_SEARCH_MAX_RESULTS: int = 5
    MCP_SERVER_URL: str = "http://localhost:8001/sse"

    MAX_MESSAGES_BEFORE_SUMMARY: int = 20  # number of messages before summarization triggers
    SUMMARY_KEEP_LAST: int = 6             # number of recent messages to keep after summarization


settings = Settings()