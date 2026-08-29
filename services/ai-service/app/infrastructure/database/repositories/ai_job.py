from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.infrastructure.database.models import AIJobRecord


class AIJobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        job_type: str,
        user_id: int | None = None,
        input_reference: str | None = None,
    ) -> AIJobRecord:
        job = AIJobRecord(
            user_id=user_id,
            job_type=job_type,
            status="queued",
            input_reference=input_reference,
        )

        self.session.add(job)
        self.session.flush()

        return job

    def get(self, job_id: int) -> AIJobRecord | None:
        return self.session.get(AIJobRecord, job_id)

    def mark_running(self, job: AIJobRecord) -> AIJobRecord:
        job.status = "running"
        job.started_at = datetime.now(UTC)
        self.session.flush()

        return job

    def mark_completed(
        self,
        job: AIJobRecord,
        *,
        result: str,
    ) -> AIJobRecord:
        job.status = "completed"
        job.result = result
        job.error = None
        job.completed_at = datetime.now(UTC)
        self.session.flush()

        return job

    def mark_failed(
        self,
        job: AIJobRecord,
        *,
        error: str,
    ) -> AIJobRecord:
        job.status = "failed"
        job.error = error
        job.completed_at = datetime.now(UTC)
        self.session.flush()

        return job