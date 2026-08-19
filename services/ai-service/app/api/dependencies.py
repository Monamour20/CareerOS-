from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.analyze_resume import AnalyzeResumeUseCase
from app.application.auth import AuthService
from app.application.career_profile_vault import CareerProfileVaultService
from app.application.onboarding import OnboardingService
from app.core.config import Settings, get_settings
from app.core.errors import AuthenticationError, DatabaseConfigurationError
from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.account import AccountRepository
from app.infrastructure.database.repositories.career_profile import CareerProfileRepository
from app.infrastructure.database.session import get_database_session, get_optional_database_session
from app.infrastructure.document.service import DocumentExtractionService
from app.infrastructure.llm.ollama import OllamaProvider

bearer_scheme = HTTPBearer(auto_error=False)


def get_analyze_resume_use_case(
    session: Annotated[Session | None, Depends(get_optional_database_session)],
) -> AnalyzeResumeUseCase:
    settings: Settings = get_settings()
    extraction_service = DocumentExtractionService(libreoffice_path=settings.libreoffice_path)
    llm_client = OllamaProvider(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        timeout_seconds=settings.ollama_timeout_seconds,
    )
    repository = CareerProfileRepository(session) if session is not None else None
    return AnalyzeResumeUseCase(
        extraction_service=extraction_service,
        llm_client=llm_client,
        career_profile_repository=repository,
    )


def get_career_profile_vault_service(
    session: Annotated[Session, Depends(get_database_session)],
) -> CareerProfileVaultService:
    if not get_settings().database_url:
        raise DatabaseConfigurationError("DATABASE_URL is not configured.")
    return CareerProfileVaultService(CareerProfileRepository(session))


def get_account_repository(
    session: Annotated[Session, Depends(get_database_session)],
) -> AccountRepository:
    if not get_settings().database_url:
        raise DatabaseConfigurationError("DATABASE_URL is not configured.")
    return AccountRepository(session)


def get_auth_service(
    repository: Annotated[AccountRepository, Depends(get_account_repository)],
) -> AuthService:
    return AuthService(repository)


def get_current_session_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("A valid bearer token is required.")
    return credentials.credentials


def get_current_user(
    token: Annotated[str, Depends(get_current_session_token)],
    repository: Annotated[AccountRepository, Depends(get_account_repository)],
) -> UserRecord:
    user = repository.get_user_by_session_token(token)
    if user is None:
        raise AuthenticationError("A valid bearer token is required.")
    return user


def get_onboarding_service(
    session: Annotated[Session, Depends(get_database_session)],
) -> OnboardingService:
    if not get_settings().database_url:
        raise DatabaseConfigurationError("DATABASE_URL is not configured.")
    account_repository = AccountRepository(session)
    vault_service = CareerProfileVaultService(CareerProfileRepository(session))
    return OnboardingService(account_repository, vault_service)
