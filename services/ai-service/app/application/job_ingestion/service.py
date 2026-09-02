from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.application.job_ingestion.normalizer import JobNormalizer
from app.application.jobs import JobService
from app.domain.job.models import Job
from app.infrastructure.database.models.job import JobRecord


@dataclass(frozen=True)
class JobIngestionResult:
    """Result of normalizing and persisting one external job."""

    record: JobRecord
    created: bool


class JobIngestionService:
    """Normalizes and persists jobs from external providers."""

    def __init__(
        self,
        *,
        normalizer: JobNormalizer,
        job_service: JobService,
    ):
        self.normalizer = normalizer
        self.job_service = job_service

    def ingest(
        self,
        *,
        source: str,
        data: dict[str, Any],
    ) -> JobRecord:
        """Normalize and upsert one external job."""
        job = self.normalizer.normalize(
            source=source,
            data=data,
        )

        return self.job_service.upsert_job(job)

    def upsert_raw_job(
        self,
        *,
        source: str,
        raw_job: dict[str, Any],
    ) -> JobIngestionResult:
        """
        Normalize and persist a raw provider job.

        The existing job is detected using the provider source and
        external ID. This lets discovery safely update jobs that have
        already been imported.
        """
        job = self.normalizer.normalize(
            source=source,
            data=raw_job,
        )

        existing = None

        if job.external_id:
            existing = self.job_service.get_job_by_external_id(
                source=source,
                external_id=job.external_id,
            )

        record = self.job_service.upsert_job(job)

        return JobIngestionResult(
            record=record,
            created=existing is None,
        )

    def normalize(
        self,
        *,
        source: str,
        data: dict[str, Any],
    ) -> Job:
        """Normalize provider-specific job data."""
        return self.normalizer.normalize(
            source=source,
            data=data,
        )