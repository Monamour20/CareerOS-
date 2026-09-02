from __future__ import annotations

from typing import Any

from app.application.job_ingestion.providers import JobSearchRequest
from app.infrastructure.job_providers.config import JobProviderConfig
from app.infrastructure.job_providers.http import JobProviderHTTPClient


class ExternalJobProvider:
    """Base adapter for HTTP-based external job providers."""

    def __init__(
        self,
        *,
        config: JobProviderConfig,
        http_client: JobProviderHTTPClient,
    ):
        self.name = config.name
        self.config = config
        self.http_client = http_client

    async def search(
        self,
        request: JobSearchRequest,
    ) -> list[dict[str, Any]]:
        """Fetch raw jobs from an external provider.

        Concrete providers should override this method because
        every provider has a different API contract.
        """

        raise NotImplementedError(
            "Concrete job providers must implement search()."
        )