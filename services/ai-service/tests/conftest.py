from collections.abc import AsyncIterator

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_analyze_resume_use_case
from app.application.analyze_resume import AnalyzeResumeUseCase
from app.domain.career_profile.models import CareerProfile
from app.infrastructure.document.service import DocumentExtractionService
from app.main import app

VALID_PROFILE = {
    "personal_information": {
        "full_name": "Ada Lovelace",
        "email": "ada@example.com",
        "phone": None,
        "location": None,
        "links": [],
        "summary": "Computing pioneer.",
    },
    "education": [],
    "experience": [],
    "skills": {"technical": ["Python"], "tools": [], "languages": [], "soft_skills": []},
    "projects": [],
    "certifications": [],
    "achievements": [],
    "career_interests": {
        "target_roles": ["Software Engineer"],
        "industries": [],
        "seniority": None,
        "strengths": [],
        "growth_areas": [],
    },
}


class FakeLLM:
    async def analyze_resume(self, resume_text: str) -> str:
        return CareerProfile.model_validate(VALID_PROFILE).model_dump_json()


@pytest.fixture
def client() -> AsyncIterator[TestClient]:
    use_case = AnalyzeResumeUseCase(
        extraction_service=DocumentExtractionService(),
        llm_client=FakeLLM(),
    )
    app.dependency_overrides[get_analyze_resume_use_case] = lambda: use_case
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
