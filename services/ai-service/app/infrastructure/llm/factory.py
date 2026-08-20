from app.core.config import Settings
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.ollama import OllamaProvider


def create_llm_client(settings: Settings) -> LLMClient:
    provider = settings.llm_provider.strip().lower()

    if provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            timeout_seconds=settings.ollama_timeout_seconds,
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
