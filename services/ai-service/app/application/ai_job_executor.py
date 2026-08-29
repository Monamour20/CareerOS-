from __future__ import annotations

import logging

from app.domain.career_profile.validator import CareerProfileValidator
from app.infrastructure.database.models import AIJobRecord
from app.infrastructure.database.repositories.ai_job import AIJobRepository
from app.infrastructure.llm.base import LLMClient

logger = logging.getLogger(__name__)


class AIJobExecutor:
    """Executes queued AI jobs using the configured LLM provider."""

    def __init__(
        self,
        repository: AIJobRepository,
        llm_client: LLMClient,
        validator: CareerProfileValidator | None = None,
    ):
        self.repository = repository
        self.llm_client = llm_client
        self.validator = validator or CareerProfileValidator()

    async def execute(self, job: AIJobRecord) -> AIJobRecord:
        self.repository.mark_running(job)

        logger.info(
            "ai_job_started",
            extra={
                "job_id": job.id,
                "job_type": job.job_type,
            },
        )

        try:
            if job.job_type != "resume_analysis":
                raise ValueError(
                    f"Unsupported AI job type: {job.job_type}"
                )

            if not job.input_reference:
                raise ValueError(
                    "Resume analysis job is missing input_reference."
                )

            llm_output = await self.llm_client.analyze_resume(
                job.input_reference
            )

            profile = self.validator.validate(llm_output)

            result = profile.model_dump_json()

            completed_job = self.repository.mark_completed(
                job,
                result=result,
            )

            logger.info(
                "ai_job_completed",
                extra={
                    "job_id": job.id,
                    "job_type": job.job_type,
                },
            )

            return completed_job

        except Exception as exc:
            error_message = str(exc) or exc.__class__.__name__

            failed_job = self.repository.mark_failed(
                job,
                error=error_message,
            )

            logger.exception(
                "ai_job_failed",
                extra={
                    "job_id": job.id,
                    "job_type": job.job_type,
                    "error": error_message,
                },
            )

            return failed_job