from app.application.job_matching import JobMatchingService
from app.domain.career_profile.models import (
    CareerProfile,
    CareerInterests,
    PersonalInformation,
    Skills,
)
from app.domain.job.models import Job, JobSkill


def make_profile() -> CareerProfile:
    return CareerProfile(
        personal_information=PersonalInformation(
            full_name="Test User",
            email="test@example.com",
        ),
        skills=Skills(
            technical=["Python", "Machine Learning", "SQL"],
            tools=["PostgreSQL", "Docker"],
            languages=["Python"],
            soft_skills=["Problem solving"],
        ),
        career_interests=CareerInterests(
            target_roles=["Machine Learning Engineer"],
            industries=["Artificial Intelligence", "Technology"],
            seniority="entry",
            strengths=["Python", "Machine Learning"],
            growth_areas=["Cloud Computing"],
        ),
    )


def make_job(**overrides) -> Job:
    data = {
        "external_id": "test-job",
        "source": "test",
        "title": "Junior Machine Learning Engineer",
        "company": "AI Test Labs",
        "location": "Navi Mumbai",
        "remote": True,
        "employment_type": "full-time",
        "seniority": "entry",
        "description": (
            "Build machine learning systems using Python, SQL, "
            "PostgreSQL and Docker."
        ),
        "skills": [
            JobSkill(name="Python", required=True),
            JobSkill(name="Machine Learning", required=True),
            JobSkill(name="SQL", required=True),
            JobSkill(name="Docker", required=False),
        ],
    }

    data.update(overrides)
    return Job(**data)


def test_matching_job_gets_high_score():
    service = JobMatchingService()

    result = service.match(
        job_id=1,
        job=make_job(),
        profile=make_profile(),
    )

    assert result.score >= 80
    assert result.score <= 100
    assert "python" in result.matched_skills
    assert "machine learning" in result.matched_skills
    assert "sql" in result.matched_skills


def test_required_missing_skill_is_reported():
    service = JobMatchingService()

    job = make_job(
        skills=[
            JobSkill(name="Python", required=True),
            JobSkill(name="Kubernetes", required=True),
        ]
    )

    result = service.match(
        job_id=1,
        job=job,
        profile=make_profile(),
    )

    assert "kubernetes" in result.missing_skills
    assert any("Missing" in reason for reason in result.reasons)


def test_optional_skill_does_not_count_as_required():
    service = JobMatchingService()

    job = make_job(
        skills=[
            JobSkill(name="Python", required=True),
            JobSkill(name="Kubernetes", required=False),
        ]
    )

    result = service.match(
        job_id=1,
        job=job,
        profile=make_profile(),
    )

    assert "python" in result.matched_skills
    assert "kubernetes" in result.missing_skills
    assert result.score >= 50


def test_skill_aliases_are_supported():
    service = JobMatchingService()

    job = make_job(
        skills=[
            JobSkill(name="ML", required=True),
            JobSkill(name="Postgres", required=True),
        ]
    )

    result = service.match(
        job_id=1,
        job=job,
        profile=make_profile(),
    )

    assert "ml" in result.matched_skills
    assert "postgres" in result.matched_skills
    assert result.missing_skills == []


def test_role_and_seniority_matching_are_reflected():
    service = JobMatchingService()

    result = service.match(
        job_id=1,
        job=make_job(
            title="Junior Machine Learning Engineer",
            seniority="entry",
        ),
        profile=make_profile(),
    )

    assert any("target career role" in reason for reason in result.reasons)
    assert any("preferred seniority" in reason for reason in result.reasons)


def test_score_never_exceeds_100():
    service = JobMatchingService()

    result = service.match(
        job_id=1,
        job=make_job(),
        profile=make_profile(),
    )

    assert 0 <= result.score <= 100