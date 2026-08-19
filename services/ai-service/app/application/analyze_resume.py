import logging
import time
from dataclasses import dataclass

from app.core.errors import InvalidFileError
from app.domain.career_profile.models import CareerProfile
from app.domain.career_profile.validator import CareerProfileValidator
from app.infrastructure.database.repositories.career_profile import (
    CareerProfileRepository,
)
from app.infrastructure.document.service import DocumentExtractionService
from app.infrastructure.llm.base import LLMClient

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResumeFile:
    filename: str
    content_type: str | None
    content: bytes


class AnalyzeResumeUseCase:
    def __init__(
        self,
        extraction_service: DocumentExtractionService,
        llm_client: LLMClient,
        validator: CareerProfileValidator | None = None,
        career_profile_repository: CareerProfileRepository | None = None,
    ):
        self.extraction_service = extraction_service
        self.llm_client = llm_client
        self.validator = validator or CareerProfileValidator()
        self.career_profile_repository = career_profile_repository

    async def execute(self, resume_file: ResumeFile) -> CareerProfile:
        if not resume_file.content:
            raise InvalidFileError("Uploaded file is empty.")

        total_start = time.perf_counter()

        logger.info(
            "resume_analysis_started",
            extra={
                "resume_filename": resume_file.filename,
                "upload_bytes": len(resume_file.content),
            },
        )

        extraction_start = time.perf_counter()

        extracted = self.extraction_service.extract(
            filename=resume_file.filename,
            content=resume_file.content,
            content_type=resume_file.content_type,
        )

        extraction_seconds = time.perf_counter() - extraction_start

        logger.info(
            "resume_extraction_completed",
            extra={
                "resume_filename": resume_file.filename,
                "detected_type": extracted.document_type,
                "extracted_characters": len(extracted.text),
                "extraction_seconds": round(extraction_seconds, 2),
            },
        )

        llm_start = time.perf_counter()

        logger.info(
            "resume_llm_started",
            extra={
                "resume_filename": resume_file.filename,
                "prompt_input_characters": len(extracted.text),
            },
        )

        llm_output = await self.llm_client.analyze_resume(extracted.text)

        llm_seconds = time.perf_counter() - llm_start

        logger.info(
            "resume_llm_completed",
            extra={
                "resume_filename": resume_file.filename,
                "llm_output_characters": len(llm_output),
                "llm_seconds": round(llm_seconds, 2),
            },
        )

        validation_start = time.perf_counter()

        profile = self.validator.validate(llm_output)

        validation_seconds = time.perf_counter() - validation_start

        logger.info(
            "resume_validation_completed",
            extra={
                "resume_filename": resume_file.filename,
                "validation_seconds": round(validation_seconds, 2),
            },
        )

        if self.career_profile_repository is not None:
            self.career_profile_repository.save(profile)

        total_seconds = time.perf_counter() - total_start

        logger.info(
            "resume_analysis_completed",
            extra={
                "resume_filename": resume_file.filename,
                "detected_type": extracted.document_type,
                "total_seconds": round(total_seconds, 2),
            },
        )

        return profile