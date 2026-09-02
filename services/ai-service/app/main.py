from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.ai_jobs import router as ai_jobs_router
from app.api.routes.auth import router as auth_router
from app.api.routes.career_intelligence import (
    router as career_intelligence_router,
)
from app.api.routes.career_profile import (
    router as career_profile_router,
)
from app.api.routes.health import router as health_router
from app.api.routes.job_matching import (
    router as job_matching_router,
)
from app.api.routes.jobs import router as jobs_router
from app.api.routes.onboarding import router as onboarding_router
from app.api.routes.recommended_jobs import (
    router as recommended_jobs_router,
)
from app.api.routes.resume_analysis import router as resume_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title="CareerOS AI Service",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in settings.cors_origins.split(",")
            if origin.strip()
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(health_router)

    app.include_router(
        auth_router,
        prefix="/api/v1",
    )

    app.include_router(
        career_profile_router,
        prefix="/api/v1",
    )

    app.include_router(
        career_intelligence_router,
        prefix="/api/v1",
    )

    app.include_router(
        onboarding_router,
        prefix="/api/v1",
    )

    app.include_router(
        resume_router,
        prefix="/api/v1",
    )

    app.include_router(
        ai_jobs_router,
        prefix="/api/v1",
    )

    # Register the static /recommended route BEFORE /{job_id}.
    app.include_router(
        recommended_jobs_router,
        prefix="/api/v1",
    )

    app.include_router(
        jobs_router,
        prefix="/api/v1",
    )

    app.include_router(
        job_matching_router,
        prefix="/api/v1",
    )

    return app


app = create_app()