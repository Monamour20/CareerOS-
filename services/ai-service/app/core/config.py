from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


SERVICE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = SERVICE_ROOT.parents[1]


class Settings(BaseSettings):
    environment: str = Field(
        default="local",
        alias="CAREEROS_ENV",
    )

    log_level: str = Field(
        default="INFO",
        alias="CAREEROS_LOG_LEVEL",
    )

    cors_origins: str = Field(
        default=(
            "http://localhost:3000,"
            "http://127.0.0.1:3000,"
            "http://localhost:3001,"
            "http://127.0.0.1:3001"
        ),
        alias="CAREEROS_CORS_ORIGINS",
    )

    max_upload_bytes: int = Field(
        default=10 * 1024 * 1024,
        alias="CAREEROS_MAX_UPLOAD_BYTES",
    )

    adzuna_app_id: str | None = None
    adzuna_app_key: str | None = None
    adzuna_country: str = "in"
    adzuna_timeout_seconds: float = 30.0
    
    # =========================
    # LLM PROVIDER
    # =========================

    llm_provider: str = Field(
        default="gemini",
        alias="LLM_PROVIDER",
    )

    # =========================
    # OLLAMA
    # =========================

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )

    ollama_model: str = Field(
        default="",
        alias="OLLAMA_MODEL",
    )

    ollama_timeout_seconds: float = Field(
        default=180.0,
        alias="OLLAMA_TIMEOUT_SECONDS",
    )

    # =========================
    # OPENAI
    # =========================

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    openai_model: str = Field(
        default="",
        alias="OPENAI_MODEL",
    )

    openai_timeout_seconds: float = Field(
        default=180.0,
        alias="OPENAI_TIMEOUT_SECONDS",
    )

    # =========================
    # GEMINI

    gemini_api_key: str | None = Field(
        default=None,
        alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-3.6-flash",
        alias="GEMINI_MODEL",
    )

    gemini_timeout_seconds: float = Field(
        default=120.0,
        alias="GEMINI_TIMEOUT_SECONDS",
    )

    # =========================
    # DOCUMENT PROCESSING
    # =========================

    libreoffice_path: str | None = Field(
        default=None,
        alias="LIBREOFFICE_PATH",
    )

    # =========================
    # DATABASE
    # =========================

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