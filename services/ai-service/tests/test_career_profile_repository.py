import os
import uuid

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.application.analyze_resume import AnalyzeResumeUseCase, ResumeFile
from app.core.config import get_settings
from app.core.errors import InvalidLLMOutputError
from app.domain.career_profile.models import CareerProfile
from app.infrastructure.database.models.user import UserRecord
from app.infrastructure.database.repositories.career_profile import CareerProfileRepository
from app.infrastructure.document.service import DocumentExtractionService
from tests.conftest import FakeLLM


def database_url() -> str | None:
    return os.getenv("TEST_DATABASE_URL") or get_settings().database_url


def rich_profile() -> CareerProfile:
    email = f"ada-{uuid.uuid4().hex}@example.com"
    return CareerProfile.model_validate(
        {
            "personal_information": {
                "full_name": "Ada Lovelace",
                "email": email,
                "phone": "555-0100",
                "location": "London",
                "links": ["https://linkedin.com/in/ada", "https://github.com/ada"],
                "summary": "Computing pioneer.",
            },
            "education": [
                {
                    "institution": "Example University",
                    "degree": "BS",
                    "field_of_study": "Computer Science",
                    "start_date": "2018",
                    "end_date": "2022",
                    "details": ["Honors"],
                }
            ],
            "experience": [
                {
                    "company": "Analytical Engines",
                    "title": "Software Engineer",
                    "location": "London",
                    "start_date": "2022",
                    "end_date": "2024",
                    "responsibilities": ["Built APIs"],
                    "technologies": ["Python"],
                }
            ],
            "skills": {
                "technical": ["Python"],
                "tools": ["Git"],
                "languages": ["English"],
                "soft_skills": ["Communication"],
            },
            "projects": [
                {
                    "name": "Resume Analyzer",
                    "description": "Analyzes resumes.",
                    "technologies": ["FastAPI"],
                    "links": ["https://github.com/ada/resume"],
                }
            ],
            "certifications": [{"name": "Cloud Basics", "issuer": "AWS", "date": "2024"}],
            "achievements": [{"title": "Automation", "description": "Reduced manual work."}],
            "career_interests": {
                "target_roles": ["AI Engineer"],
                "industries": ["HR Tech"],
                "seniority": "Entry Level",
                "strengths": ["Automation"],
                "growth_areas": ["Systems Design"],
            },
        }
    )


@pytest.fixture
def db_session():
    url = database_url()
    if not url:
        pytest.skip("Set TEST_DATABASE_URL or DATABASE_URL to run PostgreSQL Career Vault tests.")
    engine = create_engine(url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        pytest.skip(f"PostgreSQL test database is unavailable: {exc}")

    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = Session()
    created_user_ids: list[int] = []

    yield session, created_user_ids

    for user_id in created_user_ids:
        user = session.get(UserRecord, user_id)
        if user is not None:
            session.delete(user)
    session.commit()
    session.close()
    engine.dispose()


def test_database_connection(db_session):
    session, _ = db_session

    assert session.execute(text("select 1")).scalar_one() == 1


def test_create_user_and_complete_career_profile(db_session):
    session, created_user_ids = db_session
    repository = CareerProfileRepository(session)

    user_id = repository.save(rich_profile())
    created_user_ids.append(user_id)
    retrieved = repository.get_by_user_id(user_id)

    assert retrieved is not None
    assert retrieved.personal_information.full_name == "Ada Lovelace"
    assert retrieved.education[0].details == ["Honors"]
    assert retrieved.experience[0].responsibilities == ["Built APIs"]
    assert retrieved.skills.technical == ["Python"]
    assert retrieved.projects[0].technologies == ["FastAPI"]
    assert retrieved.certifications[0].issuer == "AWS"
    assert retrieved.achievements[0].title == "Automation"
    assert retrieved.career_interests.target_roles == ["AI Engineer"]


@pytest.mark.asyncio
async def test_resume_analysis_persists_validated_profile(db_session):
    session, created_user_ids = db_session
    repository = CareerProfileRepository(session)
    use_case = AnalyzeResumeUseCase(
        DocumentExtractionService(),
        FakeLLM(),
        career_profile_repository=repository,
    )

    profile = await use_case.execute(
        ResumeFile("resume.txt", "text/plain", b"Ada Lovelace\nPython")
    )
    user = session.execute(
        text("select id from users where email = :email"),
        {"email": profile.personal_information.email},
    ).first()

    assert user is not None
    created_user_ids.append(user.id)
    assert repository.get_by_user_id(user.id) is not None


class InvalidLLM:
    async def analyze_resume(self, resume_text: str) -> str:
        return "not valid json"


@pytest.mark.asyncio
async def test_invalid_career_profile_is_not_persisted(db_session):
    session, _ = db_session
    before = session.execute(text("select count(*) from users")).scalar_one()
    use_case = AnalyzeResumeUseCase(
        DocumentExtractionService(),
        InvalidLLM(),
        career_profile_repository=CareerProfileRepository(session),
    )

    with pytest.raises(InvalidLLMOutputError):
        await use_case.execute(ResumeFile("resume.txt", "text/plain", b"Invalid"))

    after = session.execute(text("select count(*) from users")).scalar_one()
    assert after == before
