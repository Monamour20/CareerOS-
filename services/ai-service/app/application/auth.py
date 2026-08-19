from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.account import AccountRepository
from app.schemas.responses import AuthResponse, UserResponse


class AuthService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def signup(self, *, full_name: str, email: str, password: str) -> AuthResponse:
        user = self.repository.create_user(full_name=full_name, email=email, password=password)
        token, expires_at = self.repository.create_session(user)
        return AuthResponse(token=token, expires_at=expires_at.isoformat(), user=user_response(user))

    def login(self, *, email: str, password: str) -> AuthResponse:
        user = self.repository.authenticate_user(email=email, password=password)
        token, expires_at = self.repository.create_session(user)
        return AuthResponse(token=token, expires_at=expires_at.isoformat(), user=user_response(user))

    def logout(self, token: str) -> None:
        self.repository.delete_session(token)


def user_response(user: UserRecord) -> UserResponse:
    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        account_type=user.account_type,
        career_status=user.career_status,
        preferred_work_mode=user.preferred_work_mode,
        career_goals=user.career_goals,
        onboarding_completed=user.onboarding_completed,
        resume_creation_requested=user.resume_creation_requested,
    )
