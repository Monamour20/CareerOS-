from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_career_profile_vault_service, get_current_user
from app.application.career_profile_vault import CareerProfileVaultService
from app.core.errors import AuthorizationError
from app.infrastructure.database.models import UserRecord
from app.schemas.requests import CareerProfileCreateRequest
from app.schemas.responses import StoredCareerProfileResponse

router = APIRouter(prefix="/career-profile", tags=["career-profile"])


@router.post("", response_model=StoredCareerProfileResponse)
async def create_career_profile(
    request: CareerProfileCreateRequest,
    service: Annotated[CareerProfileVaultService, Depends(get_career_profile_vault_service)],
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> StoredCareerProfileResponse:
    if request.user_id is not None and request.user_id != current_user.id:
        raise AuthorizationError("CareerProfile can only be saved for the authenticated user.")
    user_id = service.save(request.career_profile, user_id=current_user.id)
    profile = service.get(user_id)
    return StoredCareerProfileResponse(user_id=user_id, career_profile=profile)


@router.get("/me/current", response_model=StoredCareerProfileResponse)
async def get_my_career_profile(
    service: Annotated[CareerProfileVaultService, Depends(get_career_profile_vault_service)],
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> StoredCareerProfileResponse:
    profile = service.get(current_user.id)
    return StoredCareerProfileResponse(user_id=current_user.id, career_profile=profile)


@router.put("/me/current", response_model=StoredCareerProfileResponse)
async def update_my_career_profile(
    request: CareerProfileCreateRequest,
    service: Annotated[CareerProfileVaultService, Depends(get_career_profile_vault_service)],
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> StoredCareerProfileResponse:
    user_id = service.save(request.career_profile, user_id=current_user.id)
    profile = service.get(user_id)
    return StoredCareerProfileResponse(user_id=user_id, career_profile=profile)


@router.get("/{user_id}", response_model=StoredCareerProfileResponse)
async def get_career_profile(
    user_id: int,
    service: Annotated[CareerProfileVaultService, Depends(get_career_profile_vault_service)],
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> StoredCareerProfileResponse:
    if user_id != current_user.id:
        raise AuthorizationError("CareerProfile can only be retrieved by the authenticated user.")
    profile = service.get(user_id)
    return StoredCareerProfileResponse(user_id=user_id, career_profile=profile)
