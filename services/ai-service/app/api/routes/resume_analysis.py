from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import get_analyze_resume_use_case
from app.application.analyze_resume import AnalyzeResumeUseCase, ResumeFile
from app.core.config import get_settings
from app.core.errors import InvalidFileError
from app.schemas.responses import ResumeAnalysisResponse

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    file: Annotated[UploadFile, File()],
    use_case: Annotated[AnalyzeResumeUseCase, Depends(get_analyze_resume_use_case)],
) -> ResumeAnalysisResponse:
    content = await file.read()
    settings = get_settings()
    if len(content) > settings.max_upload_bytes:
        raise InvalidFileError(f"Uploaded file exceeds {settings.max_upload_bytes} bytes.")

    profile = await use_case.execute(
        ResumeFile(
            filename=file.filename or "resume",
            content_type=file.content_type,
            content=content,
        )
    )
    return ResumeAnalysisResponse(career_profile=profile)
