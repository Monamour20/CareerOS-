from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service, get_current_session_token, get_current_user
from app.application.auth import AuthService, user_response
from app.infrastructure.database.models import UserRecord
from app.schemas.requests import LoginRequest, SignupRequest
from app.schemas.responses import AuthResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse)
async def signup(
    request: SignupRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthResponse:
    return service.signup(
        full_name=request.full_name.strip(),
        email=request.email.strip(),
        password=request.password,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthResponse:
    return service.login(email=request.email.strip(), password=request.password)


@router.post("/logout")
async def logout(
    token: Annotated[str, Depends(get_current_session_token)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, bool]:
    service.logout(token)
    return {"ok": True}


@router.get("/me", response_model=UserResponse)
async def me(current_user: Annotated[UserRecord, Depends(get_current_user)]) -> UserResponse:
    return user_response(current_user)
