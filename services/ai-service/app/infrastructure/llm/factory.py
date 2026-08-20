from app.core.config import Settings
from app.core.errors import LLMConnectionError
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.ollama import OllamaProvider
from app.infrastructure.llm.openai import OpenAIProvider


def create_llm_client(settings: Settings) -> LLMClient:
    provider = settings.llm_provider.strip().lower()

    if provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            timeout_seconds=settings.ollama_timeout_seconds,
        )

    if provider == "openai":
        if not settings.openai_api_key:
            raise LLMConnectionError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )

        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            timeout_seconds=settings.openai_timeout_seconds,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {settings.llm_provider}"
    )