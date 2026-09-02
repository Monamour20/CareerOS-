from __future__ import annotations

import pytest

from app.application.job_ingestion.providers import JobSearchRequest
from app.infrastructure.job_providers.adzuna import AdzunaJobProvider
from app.infrastructure.job_providers.config import JobProviderConfig


class MockHTTPClient:
    def __init__(self, response: dict):
        self.response = response
        self.last_url: str | None = None
        self.last_params: dict | None = None

    async def get_json(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict:
        self.last_url = url
        self.last_params = params
        return self.response


@pytest.mark.asyncio
async def test_adzuna_provider_search() -> None:
    http_client = MockHTTPClient(
        response={
            "results": [
                {
                    "id": "123",
                    "title": "Python Developer",
                },
                {
                    "id": "456",
                    "title": "Backend Engineer",
                },
            ]
        }
    )

    provider = AdzunaJobProvider(
        config=JobProviderConfig(
            name="adzuna",
            base_url="https://api.adzuna.com/v1/api",
            credentials={
                "app_id": "test-app-id",
                "app_key": "test-app-key",
            },
        ),
        http_client=http_client,
        country="in",
    )

    jobs = await provider.search(
        JobSearchRequest(
            query="Python Developer",
            location="Mumbai",
            remote=False,
            limit=10,
        )
    )

    assert len(jobs) == 2
    assert jobs[0]["id"] == "123"
    assert jobs[1]["id"] == "456"

    assert http_client.last_url == (
        "https://api.adzuna.com/v1/api/jobs/in/1"
    )

    assert http_client.last_params == {
        "app_id": "test-app-id",
        "app_key": "test-app-key",
        "results_per_page": 10,
        "what": "Python Developer",
        "where": "Mumbai",
    }


@pytest.mark.asyncio
async def test_adzuna_provider_requires_credentials() -> None:
    provider = AdzunaJobProvider(
        config=JobProviderConfig(
            name="adzuna",
            base_url="https://api.adzuna.com/v1/api",
        ),
        http_client=MockHTTPClient(
            response={"results": []}
        ),
        country="in",
    )

    with pytest.raises(
        ValueError,
        match="app_id and app_key",
    ):
        await provider.search(
            JobSearchRequest(
                query="Python",
                limit=10,
            )
        )


@pytest.mark.asyncio
async def test_adzuna_provider_returns_empty_for_invalid_results() -> None:
    provider = AdzunaJobProvider(
        config=JobProviderConfig(
            name="adzuna",
            base_url="https://api.adzuna.com/v1/api",
            credentials={
                "app_id": "test-app-id",
                "app_key": "test-app-key",
            },
        ),
        http_client=MockHTTPClient(
            response={
                "results": None,
            }
        ),
        country="in",
    )

    jobs = await provider.search(
        JobSearchRequest(
            query="Python",
            limit=10,
        )
    )

    assert jobs == []