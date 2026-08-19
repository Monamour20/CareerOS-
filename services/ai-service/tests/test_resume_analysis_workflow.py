import pytest

from app.application.analyze_resume import AnalyzeResumeUseCase, ResumeFile
from app.core.errors import LLMConnectionError
from app.infrastructure.document.service import DocumentExtractionService
from tests.conftest import FakeLLM


class FailingLLM:
    async def analyze_resume(self, resume_text: str) -> str:
        raise LLMConnectionError("Could not connect to Ollama.")


@pytest.mark.asyncio
async def test_resume_analysis_workflow():
    use_case = AnalyzeResumeUseCase(DocumentExtractionService(), FakeLLM())

    profile = await use_case.execute(
        ResumeFile(
            filename="resume.txt",
            content_type="text/plain",
            content=b"Ada Lovelace\nPython",
        )
    )

    assert profile.personal_information.full_name == "Ada Lovelace"


@pytest.mark.asyncio
async def test_llm_failure_handling():
    use_case = AnalyzeResumeUseCase(DocumentExtractionService(), FailingLLM())

    with pytest.raises(LLMConnectionError):
        await use_case.execute(
            ResumeFile(
                filename="resume.txt",
                content_type="text/plain",
                content=b"Ada Lovelace\nPython",
            )
        )


def test_resume_analyze_endpoint(client):
    response = client.post(
        "/api/v1/resume/analyze",
        files={"file": ("resume.txt", b"Ada Lovelace\nPython", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["career_profile"]["personal_information"]["full_name"] == "Ada Lovelace"
