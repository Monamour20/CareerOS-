from dataclasses import dataclass

from app.infrastructure.database.models import AIJobRecord
from app.infrastructure.database.repositories.ai_job import AIJobRepository


@dataclass(frozen=True)
class AIJobStatus:
    id: int
    job_type: str
    status: str
    result: str | None
    error: str | None


class AIJobService:
    def __init__(self, repository: AIJobRepository):
        self.repository = repository

    def create_job(
        self,
        *,
        job_type: str,
        user_id: int | None = None,
        input_reference: str | None = None,
    ) -> AIJobRecord:
        return self.repository.create(
            job_type=job_type,
            user_id=user_id,
            input_reference=input_reference,
        )

    def get_status(self, job_id: int) -> AIJobStatus | None:
        job = self.repository.get(job_id)

        if job is None:
            return None

        return AIJobStatus(
            id=job.id,
            job_type=job.job_type,
            status=job.status,
            result=job.result,
            error=job.error,
        )