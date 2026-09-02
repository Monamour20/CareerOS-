from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_current_user,
    get_job_matching_service,
    get_job_service,
)
from app.application.career_profile_vault import CareerProfileVaultService
from app.application.job_matching import JobMatchingService
from app.application.jobs import JobService
from app.domain.job.models import Job
from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.career_profile import (
    CareerProfileRepository,
)
from app.infrastructure.database.repositories.job import job_to_domain
from app.infrastructure.database.session import get_database_session
from app.schemas.jobs import JobMatchResponse


router = APIRouter(
    prefix="/jobs",
    tags=["job-matching"],
)


@router.post(
    "/{job_id}/match",
    response_model=JobMatchResponse,
    status_code=status.HTTP_200_OK,
)
async def match_job(
    job_id: int,
    current_user: Annotated[
        UserRecord,
        Depends(get_current_user),
    ],
    job_service: Annotated[
        JobService,
        Depends(get_job_service),
    ],
    matching_service: Annotated[
        JobMatchingService,
        Depends(get_job_matching_service),
    ],
    session=Depends(get_database_session),
) -> JobMatchResponse:
    record = job_service.get_job(job_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job was not found.",
        )

    profile_service = CareerProfileVaultService(
        CareerProfileRepository(session)
    )

    try:
        profile = profile_service.get(current_user.id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career profile was not found.",
        ) from exc

    job: Job = job_to_domain(record)

    match = matching_service.match(
        job_id=record.id,
        job=job,
        profile=profile,
    )

    return JobMatchResponse(
    job_id=match.job_id,
    score=match.score,
    matched_skills=match.matched_skills,
    missing_skills=match.missing_skills,
    reasons=match.reasons,
    ) 