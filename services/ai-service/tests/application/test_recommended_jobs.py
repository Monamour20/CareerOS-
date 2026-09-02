from unittest.mock import Mock

from app.application.recommended_jobs import (
    RecommendationCategory,
    RecommendedJobsService,
)
from app.domain.career_profile.models import (
    CareerProfile,
    CareerInterests,
    PersonalInformation,
    Skills,
)
from app.domain.job.models import Job, JobMatch, JobSkill


def make_profile() -> CareerProfile:
    return CareerProfile(
        personal_information=PersonalInformation(
            full_name="Test User",
            email="test@example.com",
        ),
        skills=Skills(
            technical=[
                "Python",
                "Machine Learning",
                "SQL",
            ],
            tools=[
                "PostgreSQL",
                "Docker",
            ],
            languages=[
                "Python",
            ],
            soft_skills=[
                "Problem solving",
            ],
        ),
        career_interests=CareerInterests(
            target_roles=[
                "Machine Learning Engineer",
            ],
            industries=[
                "Artificial Intelligence",
                "Technology",
            ],
            seniority="entry",
            strengths=[
                "Python",
                "Machine Learning",
            ],
            growth_areas=[
                "Cloud Computing",
            ],
        ),
    )


def make_job(
    job_id: str,
    *,
    skills: list[JobSkill],
    title: str = "Machine Learning Engineer",
) -> Job:
    return Job(
        external_id=job_id,
        source="test",
        title=title,
        company="Test Company",
        location="Navi Mumbai",
        remote=True,
        employment_type="full-time",
        seniority="entry",
        description="Machine learning software engineering role.",
        skills=skills,
    )


def test_excellent_match_is_recommended_first():
    job_service = Mock()
    matching_service = Mock()

    record = Mock()
    record.id = 1

    job_service.list_jobs.return_value = [record]

    matching_service.match.return_value = JobMatch(
        job_id=1,
        score=95,
        matched_skills=[
            "python",
            "machine learning",
            "sql",
        ],
        missing_skills=[],
        reasons=[
            "Matches 3 required skill(s).",
            "The role closely matches a target career role.",
        ],
    )

    # Mock conversion from database record to domain job.
    service = RecommendedJobsService(
        job_service=job_service,
        matching_service=matching_service,
    )

    job = make_job(
        "excellent",
        skills=[
            JobSkill(name="Python", required=True),
            JobSkill(name="Machine Learning", required=True),
            JobSkill(name="SQL", required=True),
        ],
    )

    import app.application.recommended_jobs as module

    original_converter = module.job_to_domain
    module.job_to_domain = lambda _: job

    try:
        result = service.recommend(
            profile=make_profile(),
            limit=20,
            offset=0,
        )
    finally:
        module.job_to_domain = original_converter

    assert len(result) == 1
    assert result[0].category == RecommendationCategory.EXCELLENT
    assert result[0].match.score == 95


def test_low_score_job_is_rejected():
    job_service = Mock()
    matching_service = Mock()

    record = Mock()
    record.id = 1

    job_service.list_jobs.return_value = [record]

    matching_service.match.return_value = JobMatch(
        job_id=1,
        score=35,
        matched_skills=[],
        missing_skills=[
            "python",
            "machine learning",
        ],
        reasons=[],
    )

    service = RecommendedJobsService(
        job_service=job_service,
        matching_service=matching_service,
    )

    job = make_job(
        "low-score",
        skills=[
            JobSkill(name="Python", required=True),
            JobSkill(name="Machine Learning", required=True),
        ],
    )

    import app.application.recommended_jobs as module

    original_converter = module.job_to_domain
    module.job_to_domain = lambda _: job

    try:
        result = service.recommend(
            profile=make_profile(),
        )
    finally:
        module.job_to_domain = original_converter

    assert result == []


def test_more_than_half_required_skills_can_still_be_recommended():
    job_service = Mock()
    matching_service = Mock()

    record = Mock()
    record.id = 1

    job_service.list_jobs.return_value = [record]

    matching_service.match.return_value = JobMatch(
        job_id=1,
        score=72,
        matched_skills=[
            "python",
            "machine learning",
        ],
        missing_skills=[
            "kubernetes",
        ],
        reasons=[
            "Matches 2 required skill(s).",
            "Missing 1 required skill(s): kubernetes.",
        ],
    )

    service = RecommendedJobsService(
        job_service=job_service,
        matching_service=matching_service,
    )

    job = make_job(
        "skill-gap",
        skills=[
            JobSkill(name="Python", required=True),
            JobSkill(name="Machine Learning", required=True),
            JobSkill(name="Kubernetes", required=True),
        ],
    )

    import app.application.recommended_jobs as module

    original_converter = module.job_to_domain
    module.job_to_domain = lambda _: job

    try:
        result = service.recommend(
            profile=make_profile(),
        )
    finally:
        module.job_to_domain = original_converter

    assert len(result) == 1
    assert result[0].category == RecommendationCategory.SKILL_GAP


def test_less_than_half_required_skills_are_rejected():
    job_service = Mock()
    matching_service = Mock()

    record = Mock()
    record.id = 1

    job_service.list_jobs.return_value = [record]

    matching_service.match.return_value = JobMatch(
        job_id=1,
        score=60,
        matched_skills=["python"],
        missing_skills=[
            "machine learning",
            "sql",
            "kubernetes",
        ],
        reasons=[
            "Matches 1 required skill(s).",
            "Missing 3 required skill(s).",
        ],
    )

    service = RecommendedJobsService(
        job_service=job_service,
        matching_service=matching_service,
    )

    job = make_job(
        "weak-skills",
        skills=[
            JobSkill(name="Python", required=True),
            JobSkill(name="Machine Learning", required=True),
            JobSkill(name="SQL", required=True),
            JobSkill(name="Kubernetes", required=True),
        ],
    )

    import app.application.recommended_jobs as module

    original_converter = module.job_to_domain
    module.job_to_domain = lambda _: job

    try:
        result = service.recommend(
            profile=make_profile(),
        )
    finally:
        module.job_to_domain = original_converter

    assert result == []


def test_recommendations_are_sorted_by_category_then_score():
    service = RecommendedJobsService(
        job_service=Mock(),
        matching_service=Mock(),
    )

    excellent_job = make_job(
        "excellent",
        skills=[
            JobSkill(name="Python", required=True),
        ],
    )

    strong_job = make_job(
        "strong",
        skills=[
            JobSkill(name="Python", required=True),
        ],
    )

    potential_job = make_job(
        "potential",
        skills=[
            JobSkill(name="Python", required=True),
        ],
    )

    service.job_service.list_jobs.return_value = [
        Mock(id=1),
        Mock(id=2),
        Mock(id=3),
    ]

    matches = {
        1: JobMatch(
            job_id=1,
            score=88,
            matched_skills=["python"],
            missing_skills=[],
            reasons=[],
        ),
        2: JobMatch(
            job_id=2,
            score=75,
            matched_skills=["python"],
            missing_skills=[],
            reasons=[],
        ),
        3: JobMatch(
            job_id=3,
            score=55,
            matched_skills=["python"],
            missing_skills=[],
            reasons=[],
        ),
    }

    service.matching_service.match.side_effect = lambda **kwargs: matches[
        kwargs["job_id"]
    ]

    import app.application.recommended_jobs as module

    jobs = {
        1: excellent_job,
        2: strong_job,
        3: potential_job,
    }

    original_converter = module.job_to_domain
    module.job_to_domain = lambda record: jobs[record.id]

    try:
        result = service.recommend(
            profile=make_profile(),
        )
    finally:
        module.job_to_domain = original_converter

    assert [item.job_id for item in result] == [1, 2, 3]
    assert result[0].category == RecommendationCategory.EXCELLENT
    assert result[1].category == RecommendationCategory.STRONG
    assert result[2].category == RecommendationCategory.POTENTIAL