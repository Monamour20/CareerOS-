from __future__ import annotations

from typing import Any, Protocol


class JobProvider(Protocol):
    """Contract that every external job provider must implement."""

    @property
    def name(self) -> str:
        """Return the stable provider identifier."""

    async def search(
        self,
        *,
        query: str,
        location: str | None = None,
        remote: bool | None = None,
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        """
        Search the external provider and return raw job dictionaries.

        Provider-specific response formats must remain inside the provider
        implementation. The ingestion layer will normalize them.
        """