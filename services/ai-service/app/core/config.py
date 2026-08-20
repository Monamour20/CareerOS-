from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

SERVICE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = SERVICE_ROOT.parents[1]


class Settings(BaseSettings):
    environment: str = Field(default="local", alias="CAREEROS_ENV")
    log_level: str = Field(default="INFO", alias="CAREEROS_LOG_LEVEL")

    max_upload_bytes: int = Field(
        default=10 * 1024 * 1024,
        alias="CAREEROS_MAX_UPLOAD_BYTES",
    )

    llm_provider: str = Field(
        default="ollama",
        alias="LLM_PROVIDER",
    )

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )

    ollama_model: str = Field(
        default="qwen3.5:9b",
        alias="OLLAMA_MODEL",
    )

    ollama_timeout_seconds: float = Field(
        default=180.0,
        alias="OLLAMA_TIMEOUT_SECONDS",
    )

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    openai_model: str = Field(
        default="gpt-5.6-luna",
        alias="OPENAI_MODEL",
    )

    openai_timeout_seconds: float = Field(
        default=180.0,
        alias="OPENAI_TIMEOUT_SECONDS",
    )

    libreoffice_path: str | None = Field(
        default=None,
        alias="LIBREOFFICE_PATH",
    )

    database_url: str | None = Field(
        default=None,
        alias="DATABASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=(REPO_ROOT / ".env", SERVICE_ROOT / ".env"),
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()