from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_career_intelligence_service
from app.application.career_intelligence.service import CareerIntelligenceService
from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.career_profile import CareerProfileRepository
from app.infrastructure.database.session import get_database_session
from app.core.errors import DatabaseConfigurationError
from app.core.config import get_settings
from app.application.career_profile_vault import CareerProfileVaultService

router = APIRouter(
    prefix="/career-intelligence",
    tags=["career-intelligence"],
)


@router.post("/analyze")
async def analyze_career(
    service: Annotated[
        CareerIntelligenceService,
        Depends(get_career_intelligence_service),
    ],
    current_user: Annotated[UserRecord, Depends(get_current_user)],
    session=Depends(get_database_session),
):
    settings = get_settings()

    if not settings.database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    profile = CareerProfileVaultService(
        CareerProfileRepository(session)
    ).get(current_user.id)

    interests = profile.career_interests

    context = service.build_context(
        summary=profile.personal_information.summary or "",
        skills=(
            profile.skills.technical
            + profile.skills.tools
            + profile.skills.languages
            + profile.skills.soft_skills
        ),
        experiences=[
            f"{item.title or ''} at {item.company or ''}: "
            + "; ".join(item.responsibilities)
            for item in profile.experience
        ],
        education=[
            f"{item.degree or ''} in {item.field_of_study or ''} "
            f"at {item.institution or ''}"
            for item in profile.education
        ],
        projects=[
            f"{item.name or ''}: {item.description or ''}"
            for item in profile.projects
        ],
        certifications=[
            f"{item.name or ''} - {item.issuer or ''}"
            for item in profile.certifications
        ],
        preferences=(
            interests.target_roles
            + interests.industries
            + interests.strengths
            + interests.growth_areas
        ),
    )

    analysis = await service.analyze(context)

    return {
        "career_analysis": analysis,
    }
