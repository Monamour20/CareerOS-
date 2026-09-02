from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class JobSearchRequest:
    """Normalized request for searching jobs."""

    query: str | None = None
    location: str | None = None
    remote: bool | None = None
    limit: int = 20


class JobProvider(Protocol):
    """Contract implemented by every job provider."""

    name: str

    async def search(
        self,
        request: JobSearchRequest,
    ) -> list[dict[str, Any]]:
        """Return raw jobs from an external provider."""


class JobProviderRegistry:
    """Provides access to registered job providers."""

    def __init__(
        self,
        *,
        providers: list[JobProvider],
    ):
        self._providers = {
            provider.name: provider
            for provider in providers
        }

    def get(self, name: str) -> JobProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise ValueError(
                f"Unknown job provider: {name}"
            ) from exc

    def list_providers(self) -> list[str]:
        return sorted(self._providers)