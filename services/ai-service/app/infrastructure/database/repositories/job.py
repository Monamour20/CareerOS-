from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.core.errors import ConflictError, DatabaseOperationError
from app.domain.job.models import Job, JobSkill
from app.infrastructure.database.models.job import JobRecord
from app.infrastructure.database.models.job_skill import JobSkillRecord


class JobRepository:
    """Persists and retrieves normalized jobs."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, job: Job) -> JobRecord:
        record = JobRecord(
            external_id=job.external_id,
            source=job.source,
            title=job.title,
            company=job.company,
            location=job.location,
            remote=job.remote,
            employment_type=job.employment_type,
            seniority=job.seniority,
            description=job.description,
            application_url=job.application_url,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            currency=job.currency,
            posted_at=job.posted_at,
            expires_at=job.expires_at,
        )

        record.skills = [
            JobSkillRecord(
                name=skill.name,
                required=skill.required,
            )
            for skill in job.skills
        ]

        self.session.add(record)

        try:
            self.session.commit()
            self.session.refresh(record)
            return record

        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError("Could not create job.") from exc

        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not create job.") from exc

    def get_by_id(self, job_id: int) -> JobRecord | None:
        statement = (
            select(JobRecord)
            .where(JobRecord.id == job_id)
            .options(selectinload(JobRecord.skills))
        )

        return self.session.scalars(statement).first()

    def get_by_external_id(
        self,
        *,
        source: str,
        external_id: str,
    ) -> JobRecord | None:
        statement = (
            select(JobRecord)
            .where(JobRecord.source == source)
            .where(JobRecord.external_id == external_id)
            .options(selectinload(JobRecord.skills))
        )

        return self.session.scalars(statement).first()

    def list_jobs(
        self,
        *,
        source: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[JobRecord]:
        statement = (
            select(JobRecord)
            .options(selectinload(JobRecord.skills))
            .order_by(JobRecord.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        if source is not None:
            statement = statement.where(JobRecord.source == source)

        return list(self.session.scalars(statement).all())

    def upsert(self, job: Job) -> JobRecord:
        """
        Create a job if it does not exist.

        If the source provides an external ID and a matching job already
        exists, update the existing record instead.
        """

        existing = None

        if job.external_id:
            existing = self.get_by_external_id(
                source=job.source,
                external_id=job.external_id,
            )

        if existing is None:
            return self.create(job)

        existing.title = job.title
        existing.company = job.company
        existing.location = job.location
        existing.remote = job.remote
        existing.employment_type = job.employment_type
        existing.seniority = job.seniority
        existing.description = job.description
        existing.application_url = job.application_url
        existing.salary_min = job.salary_min
        existing.salary_max = job.salary_max
        existing.currency = job.currency
        existing.posted_at = job.posted_at
        existing.expires_at = job.expires_at

        existing.skills.clear()

        existing.skills.extend(
            JobSkillRecord(
                name=skill.name,
                required=skill.required,
            )
            for skill in job.skills
        )

        try:
            self.session.commit()
            self.session.refresh(existing)
            return existing

        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not update job.") from exc

    def delete(self, job_id: int) -> bool:
        record = self.get_by_id(job_id)

        if record is None:
            return False

        try:
            self.session.delete(record)
            self.session.commit()
            return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not delete job.") from exc


def job_to_domain(record: JobRecord) -> Job:
    """Convert a database job record into the domain representation."""

    return Job(
        external_id=record.external_id,
        source=record.source,
        title=record.title,
        company=record.company,
        location=record.location,
        remote=record.remote,
        employment_type=record.employment_type,
        seniority=record.seniority,
        description=record.description,
        application_url=record.application_url,
        salary_min=record.salary_min,
        salary_max=record.salary_max,
        currency=record.currency,
        posted_at=record.posted_at,
        expires_at=record.expires_at,
        skills=[
            JobSkill(
                name=skill.name,
                required=skill.required,
            )
            for skill in record.skills
        ],
    )