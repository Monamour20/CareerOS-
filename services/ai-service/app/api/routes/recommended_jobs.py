from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import (
    get_current_user,
    get_recommended_jobs_service,
)
from app.application.career_profile_vault import CareerProfileVaultService
from app.application.recommended_jobs import RecommendedJobsService
from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.career_profile import (
    CareerProfileRepository,
)
from app.infrastructure.database.session import get_database_session
from app.schemas.jobs import JobMatchResponse


router = APIRouter(
    prefix="/jobs",
    tags=["job-recommendations"],
)


@router.get(
    "/recommended",
    response_model=list[JobMatchResponse],
)
async def get_recommended_jobs(
    current_user: Annotated[
        UserRecord,
        Depends(get_current_user),
    ],
    service: Annotated[
        RecommendedJobsService,
        Depends(get_recommended_jobs_service),
    ],
    session=Depends(get_database_session),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
) -> list[JobMatchResponse]:
    profile_service = CareerProfileVaultService(
        CareerProfileRepository(session)
    )

    profile = profile_service.get(current_user.id)

    recommendations = service.recommend(
        profile=profile,
        limit=limit,
        offset=offset,
    )

    return [
        JobMatchResponse(
            job_id=item.job_id,
            score=item.match.score,
            category=item.category.value,
            matched_skills=item.match.matched_skills,
            missing_skills=item.match.missing_skills,
            reasons=item.match.reasons,
        )
        for item in recommendations
    ]