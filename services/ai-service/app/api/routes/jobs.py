from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import (
    get_job_discovery_service,
    get_job_service,
)
from app.application.job_ingestion.discovery import JobDiscoveryService
from app.application.job_ingestion.providers import JobSearchRequest
from app.application.jobs import JobService
from app.domain.job.models import Job
from app.schemas.jobs import (
    JobDiscoveryResponse,
    JobListResponse,
    JobResponse,
)


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    job: Job,
    service: Annotated[
        JobService,
        Depends(get_job_service),
    ],
) -> JobResponse:
    record = service.upsert_job(job)

    return JobResponse.model_validate(record)


@router.post(
    "/discover",
    response_model=JobDiscoveryResponse,
    status_code=status.HTTP_200_OK,
)
async def discover_jobs(
    request: JobSearchRequest,
    service: Annotated[
        JobDiscoveryService,
        Depends(get_job_discovery_service),
    ],
    source: str = Query(
        default="mock",
        min_length=1,
    ),
) -> JobDiscoveryResponse:
    try:
        result = await service.search(
            source=source,
            request=request,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return JobDiscoveryResponse(
        source=result.source,
        discovered=result.discovered,
        created=result.created,
        updated=result.updated,
        jobs=[
            JobResponse.model_validate(job)
            for job in result.jobs
        ],
    )


@router.get(
    "",
    response_model=JobListResponse,
)
async def list_jobs(
    service: Annotated[
        JobService,
        Depends(get_job_service),
    ],
    source: str | None = Query(
        default=None,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
) -> JobListResponse:
    records = service.list_jobs(
        source=source,
        limit=limit,
        offset=offset,
    )

    return JobListResponse(
        jobs=[
            JobResponse.model_validate(record)
            for record in records
        ],
        limit=limit,
        offset=offset,
    )

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
async def get_job(
    job_id: int,
    service: Annotated[
        JobService,
        Depends(get_job_service),
    ],
) -> JobResponse:
    record = service.get_job(job_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job was not found.",
        )

    return JobResponse.model_validate(record)


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_job(
    job_id: int,
    service: Annotated[
        JobService,
        Depends(get_job_service),
    ],
) -> None:
    deleted = service.delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job was not found.",
        )