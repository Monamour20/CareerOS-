from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_ai_job_executor, get_ai_job_service
from app.application.ai_job_executor import AIJobExecutor
from app.application.ai_jobs import AIJobService
from app.schemas.ai_jobs import (
    AIJobCreateRequest,
    AIJobCreateResponse,
    AIJobStatusResponse,
)

router = APIRouter(prefix="/ai-jobs", tags=["ai-jobs"])


@router.post(
    "",
    response_model=AIJobCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_ai_job(
    request: AIJobCreateRequest,
    service: Annotated[AIJobService, Depends(get_ai_job_service)],
    executor: Annotated[AIJobExecutor, Depends(get_ai_job_executor)],
) -> AIJobCreateResponse:
    job = service.create_job(
        job_type=request.job_type,
        input_reference=request.input_reference,
    )

    await executor.execute(job)

    return AIJobCreateResponse.model_validate(job)


@router.get(
    "/{job_id}",
    response_model=AIJobStatusResponse,
)
def get_ai_job(
    job_id: int,
    service: Annotated[AIJobService, Depends(get_ai_job_service)],
) -> AIJobStatusResponse:
    job = service.get_status(job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI job not found.",
        )

    return AIJobStatusResponse.model_validate(job)