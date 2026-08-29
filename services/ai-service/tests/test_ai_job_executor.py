import pytest

from app.application.ai_job_executor import AIJobExecutor
from app.domain.career_profile.validator import CareerProfileValidator
from app.infrastructure.database.models import AIJobRecord


class FakeLLM:
    async def analyze_resume(self, resume_text: str) -> str:
        return """
        {
            "personal_information": {
                "full_name": "Ada Lovelace",
                "email": null,
                "phone": null,
                "location": null,
                "links": [],
                "summary": "Pioneer in analytical computing"
            },
            "education": [],
            "experience": [],
            "skills": {
                "technical": ["Python"],
                "tools": [],
                "languages": [],
                "soft_skills": []
            },
            "projects": [],
            "certifications": [],
            "achievements": [],
            "career_interests": {
                "target_roles": ["Software Engineer"],
                "industries": [],
                "seniority": null,
                "strengths": ["Programming"],
                "growth_areas": []
            }
        }
        """


class FailingLLM:
    async def analyze_resume(self, resume_text: str) -> str:
        raise RuntimeError("LLM unavailable")


class FakeRepository:
    def mark_running(self, job: AIJobRecord) -> AIJobRecord:
        job.status = "running"
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
        return job

    def mark_failed(
        self,
        job: AIJobRecord,
        *,
        error: str,
    ) -> AIJobRecord:
        job.status = "failed"
        job.error = error
        return job


@pytest.mark.asyncio
async def test_ai_job_executor_completes_resume_analysis():
    job = AIJobRecord(
        id=1,
        job_type="resume_analysis",
        status="queued",
        input_reference="Ada Lovelace\nPython",
    )

    executor = AIJobExecutor(
        repository=FakeRepository(),
        llm_client=FakeLLM(),
        validator=CareerProfileValidator(),
    )

    result = await executor.execute(job)

    assert result.status == "completed"
    assert result.result is not None
    assert "Ada Lovelace" in result.result
    assert result.error is None


@pytest.mark.asyncio
async def test_ai_job_executor_marks_failed_when_llm_fails():
    job = AIJobRecord(
        id=2,
        job_type="resume_analysis",
        status="queued",
        input_reference="Ada Lovelace\nPython",
    )

    executor = AIJobExecutor(
        repository=FakeRepository(),
        llm_client=FailingLLM(),
        validator=CareerProfileValidator(),
    )

    result = await executor.execute(job)

    assert result.status == "failed"
    assert result.error == "LLM unavailable"


@pytest.mark.asyncio
async def test_ai_job_executor_rejects_missing_input():
    job = AIJobRecord(
        id=3,
        job_type="resume_analysis",
        status="queued",
        input_reference=None,
    )

    executor = AIJobExecutor(
        repository=FakeRepository(),
        llm_client=FakeLLM(),
        validator=CareerProfileValidator(),
    )

    result = await executor.execute(job)

    assert result.status == "failed"
    assert result.error == "Resume analysis job is missing input_reference."


@pytest.mark.asyncio
async def test_ai_job_executor_rejects_unknown_job_type():
    job = AIJobRecord(
        id=4,
        job_type="unknown",
        status="queued",
        input_reference="test",
    )

    executor = AIJobExecutor(
        repository=FakeRepository(),
        llm_client=FakeLLM(),
        validator=CareerProfileValidator(),
    )

    result = await executor.execute(job)

    assert result.status == "failed"
    assert result.error == "Unsupported AI job type: unknown"