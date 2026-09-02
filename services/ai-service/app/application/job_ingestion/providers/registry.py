from __future__ import annotations

from app.application.job_ingestion.providers.base import JobProvider


class JobProviderRegistry:
    """Resolves job providers by their stable source name."""

    def __init__(self, providers: list[JobProvider]):
        self._providers = {
            provider.name: provider
            for provider in providers
        }

    def get(self, name: str) -> JobProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._providers))

            raise ValueError(
                f"Unknown job provider '{name}'. "
                f"Available providers: {available or 'none'}."
            ) from exc

    def names(self) -> list[str]:
        return sorted(self._providers)