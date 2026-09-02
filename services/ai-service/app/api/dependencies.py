from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.recommended_jobs import RecommendedJobsService
from app.application.job_matching import JobMatchingService
from app.application.ai_gateway import AIGateway
from app.application.ai_job_executor import AIJobExecutor
from app.application.ai_jobs import AIJobService
from app.application.analyze_resume import AnalyzeResumeUseCase
from app.application.auth import AuthService
from app.application.career_intelligence.service import CareerIntelligenceService
from app.application.career_profile_vault import CareerProfileVaultService
from app.application.job_ingestion.discovery import JobDiscoveryService
from app.application.job_ingestion.normalizer import JobNormalizer
from app.application.job_ingestion.providers import JobProviderRegistry
from app.application.job_ingestion.service import JobIngestionService
from app.application.jobs import JobService
from app.application.onboarding import OnboardingService
from app.core.config import Settings, get_settings
from app.core.errors import (
    AuthenticationError,
    DatabaseConfigurationError,
)
from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.account import AccountRepository
from app.infrastructure.database.repositories.ai_job import AIJobRepository
from app.infrastructure.database.repositories.career_profile import (
    CareerProfileRepository,
)
from app.infrastructure.database.repositories.job import JobRepository
from app.infrastructure.database.session import (
    get_database_session,
    get_optional_database_session,
)
from app.infrastructure.document.service import DocumentExtractionService
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.job_providers import (
    AdzunaJobProvider,
    JobProviderConfig,
    MockJobProvider,
)
from app.infrastructure.job_providers.http import JobProviderHTTPClient


bearer_scheme = HTTPBearer(auto_error=False)


def get_analyze_resume_use_case(
    session: Annotated[
        Session | None,
        Depends(get_optional_database_session),
    ],
) -> AnalyzeResumeUseCase:
    settings: Settings = get_settings()

    extraction_service = DocumentExtractionService(
        libreoffice_path=settings.libreoffice_path,
    )

    llm_client = create_llm_client(settings)

    repository = (
        CareerProfileRepository(session)
        if session is not None
        else None
    )

    return AnalyzeResumeUseCase(
        extraction_service=extraction_service,
        llm_client=llm_client,
        career_profile_repository=repository,
    )


def get_career_profile_vault_service(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> CareerProfileVaultService:
    if not get_settings().database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    return CareerProfileVaultService(
        CareerProfileRepository(session)
    )


def get_account_repository(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> AccountRepository:
    if not get_settings().database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    return AccountRepository(session)


def get_auth_service(
    repository: Annotated[
        AccountRepository,
        Depends(get_account_repository),
    ],
) -> AuthService:
    return AuthService(repository)


def get_current_session_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError(
            "A valid bearer token is required."
        )

    return credentials.credentials


def get_current_user(
    token: Annotated[
        str,
        Depends(get_current_session_token),
    ],
    repository: Annotated[
        AccountRepository,
        Depends(get_account_repository),
    ],
) -> UserRecord:
    user = repository.get_user_by_session_token(token)

    if user is None:
        raise AuthenticationError(
            "A valid bearer token is required."
        )

    return user


def get_onboarding_service(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> OnboardingService:
    if not get_settings().database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    account_repository = AccountRepository(session)

    vault_service = CareerProfileVaultService(
        CareerProfileRepository(session)
    )

    return OnboardingService(
        account_repository,
        vault_service,
    )


def get_ai_job_service(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> AIJobService:
    if not get_settings().database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    return AIJobService(
        AIJobRepository(session)
    )


def get_ai_job_executor(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> AIJobExecutor:
    settings: Settings = get_settings()

    if not settings.database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    return AIJobExecutor(
        repository=AIJobRepository(session),
        llm_client=create_llm_client(settings),
    )


def get_career_intelligence_service(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> CareerIntelligenceService:
    settings = get_settings()

    if not settings.database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    return CareerIntelligenceService(
        ai_gateway=AIGateway(
            create_llm_client(settings)
        )
    )


def get_job_service(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> JobService:
    settings = get_settings()

    if not settings.database_url:
        raise DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    return JobService(
        JobRepository(session)
    )


def get_job_ingestion_service(
    job_service: Annotated[
        JobService,
        Depends(get_job_service),
    ],
) -> JobIngestionService:
    return JobIngestionService(
        normalizer=JobNormalizer(),
        job_service=job_service,
    )


def get_job_provider_registry() -> JobProviderRegistry:
    settings = get_settings()

    providers = [
        MockJobProvider(),
    ]

    if settings.adzuna_app_id and settings.adzuna_app_key:
        adzuna_config = JobProviderConfig(
            name="adzuna",
            base_url="https://api.adzuna.com/v1/api",
            timeout_seconds=settings.adzuna_timeout_seconds,
            credentials={
                "app_id": settings.adzuna_app_id,
                "app_key": settings.adzuna_app_key,
            },
        )

        providers.append(
            AdzunaJobProvider(
                config=adzuna_config,
                http_client=JobProviderHTTPClient(
                    timeout_seconds=settings.adzuna_timeout_seconds,
                ),
                country=settings.adzuna_country,
            )
        )

    return JobProviderRegistry(
        providers=providers,
    )


def get_job_discovery_service(
    ingestion_service: Annotated[
        JobIngestionService,
        Depends(get_job_ingestion_service),
    ],
    provider_registry: Annotated[
        JobProviderRegistry,
        Depends(get_job_provider_registry),
    ],
) -> JobDiscoveryService:
    return JobDiscoveryService(
        provider_registry=provider_registry,
        ingestion_service=ingestion_service,
    )

def get_job_matching_service() -> JobMatchingService:
    return JobMatchingService()

def get_recommended_jobs_service(
    job_service: Annotated[JobService, Depends(get_job_service)],
    matching_service: Annotated[
        JobMatchingService,
        Depends(get_job_matching_service),
    ],
) -> RecommendedJobsService:
    return RecommendedJobsService(
        job_service=job_service,
        matching_service=matching_service,
    )