from __future__ import annotations

from dataclasses import dataclass

from app.application.job_ingestion.providers import (
    JobProviderRegistry,
    JobSearchRequest,
)
from app.application.job_ingestion.service import JobIngestionService
from app.infrastructure.database.models.job import JobRecord


@dataclass(frozen=True)
class JobDiscoveryResult:
    """Result of discovering and persisting external jobs."""

    source: str
    discovered: int
    created: int
    updated: int
    jobs: list[JobRecord]


class JobDiscoveryService:
    """Discovers jobs through providers and persists normalized jobs."""

    def __init__(
        self,
        *,
        provider_registry: JobProviderRegistry,
        ingestion_service: JobIngestionService,
    ):
        self.provider_registry = provider_registry
        self.ingestion_service = ingestion_service

    async def search(
        self,
        *,
        source: str,
        request: JobSearchRequest,
    ) -> JobDiscoveryResult:
        provider = self.provider_registry.get(source)

        raw_jobs = await provider.search(request)

        persisted_jobs: list[JobRecord] = []
        created = 0
        updated = 0

        for raw_job in raw_jobs:
            result = self.ingestion_service.upsert_raw_job(
                source=source,
                raw_job=raw_job,
            )

            persisted_jobs.append(result.record)

            if result.created:
                created += 1
            else:
                updated += 1

        return JobDiscoveryResult(
            source=source,
            discovered=len(raw_jobs),
            created=created,
            updated=updated,
            jobs=persisted_jobs,
        )