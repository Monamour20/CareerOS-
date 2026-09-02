from __future__ import annotations

from dataclasses import dataclass

from app.domain.job.models import Job
from app.infrastructure.database.models.job import JobRecord
from app.infrastructure.database.repositories.job import JobRepository


@dataclass(frozen=True)
class JobUpsertResult:
    """Result of creating or updating a normalized job."""

    record: JobRecord
    created: bool


class JobService:
    """Application service for normalized CareerOS jobs."""

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job(self, job: Job) -> JobRecord:
        return self.repository.create(job)

    def upsert_job(self, job: Job) -> JobRecord:
        return self.repository.upsert(job)

    def upsert_job_with_result(self, job: Job) -> JobUpsertResult:
        existing = None

        if job.external_id:
            existing = self.repository.get_by_external_id(
                source=job.source,
                external_id=job.external_id,
            )

        record = self.repository.upsert(job)

        return JobUpsertResult(
            record=record,
            created=existing is None,
        )

    def get_job(self, job_id: int) -> JobRecord | None:
        return self.repository.get_by_id(job_id)

    def get_job_by_external_id(
        self,
        *,
        source: str,
        external_id: str,
    ) -> JobRecord | None:
        return self.repository.get_by_external_id(
            source=source,
            external_id=external_id,
        )

    def list_jobs(
        self,
        *,
        source: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[JobRecord]:
        return self.repository.list_jobs(
            source=source,
            limit=limit,
            offset=offset,
        )

    def delete_job(self, job_id: int) -> bool:
        return self.repository.delete(job_id)