from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_onboarding_service
from app.application.onboarding import OnboardingService
from app.infrastructure.database.models import UserRecord
from app.schemas.requests import OnboardingCareerProfileRequest
from app.schemas.responses import StoredCareerProfileResponse

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("/career-profile", response_model=StoredCareerProfileResponse)
async def complete_onboarding(
    request: OnboardingCareerProfileRequest,
    service: Annotated[OnboardingService, Depends(get_onboarding_service)],
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> StoredCareerProfileResponse:
    user_id = service.complete(
        current_user,
        career_status=request.career_status,
        preferred_work_mode=request.preferred_work_mode,
        career_goals=request.career_goals,
        resume_creation_requested=request.resume_creation_requested,
        career_profile=request.career_profile,
    )
    return StoredCareerProfileResponse(user_id=user_id, career_profile=request.career_profile)
