from __future__ import annotations

from typing import Any

from app.application.job_ingestion.providers import JobSearchRequest
from app.infrastructure.job_providers.config import JobProviderConfig
from app.infrastructure.job_providers.external import ExternalJobProvider
from app.infrastructure.job_providers.http import JobProviderHTTPClient


class AdzunaJobProvider(ExternalJobProvider):
    """Adzuna implementation of the CareerOS job provider contract."""

    def __init__(
        self,
        *,
        config: JobProviderConfig,
        http_client: JobProviderHTTPClient,
        country: str = "in",
    ):
        super().__init__(
            config=config,
            http_client=http_client,
        )

        self.country = country

    async def search(
        self,
        request: JobSearchRequest,
    ) -> list[dict[str, Any]]:
        credentials = self.config.credentials or {}

        app_id = credentials.get("app_id")
        app_key = credentials.get("app_key")

        if not app_id or not app_key:
            raise ValueError(
                "Adzuna app_id and app_key are required."
            )

        params: dict[str, Any] = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": request.limit,
        }

        if request.query:
            params["what"] = request.query

        if request.location:
            params["where"] = request.location

        if request.remote is True:
            params["what_and"] = "remote"

        url = (
            f"{self.config.base_url}/jobs/"
            f"{self.country}/1"
        )

        response = await self.http_client.get_json(
            url=url,
            params=params,
        )

        results = response.get("results", [])

        if not isinstance(results, list):
            return []

        return [
            job
            for job in results
            if isinstance(job, dict)
        ]