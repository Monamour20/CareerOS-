import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class CareerOSError(Exception):
    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UnsupportedFileError(CareerOSError):
    status_code = 415
    error_code = "unsupported_file"


class InvalidFileError(CareerOSError):
    status_code = 400
    error_code = "invalid_file"


class CorruptedDocumentError(CareerOSError):
    status_code = 400
    error_code = "corrupted_document"


class OCRFailureError(CareerOSError):
    status_code = 422
    error_code = "ocr_failure"


class EmptyExtractedTextError(CareerOSError):
    status_code = 422
    error_code = "empty_extracted_text"


class LLMConnectionError(CareerOSError):
    status_code = 503
    error_code = "llm_connection_failure"


class LLMTimeoutError(CareerOSError):
    status_code = 504
    error_code = "llm_timeout"


class InvalidLLMOutputError(CareerOSError):
    status_code = 502
    error_code = "invalid_llm_output"


class CareerProfileValidationError(CareerOSError):
    status_code = 502
    error_code = "career_profile_validation_failure"


class DatabaseConfigurationError(CareerOSError):
    status_code = 503
    error_code = "database_configuration_error"


class DatabaseOperationError(CareerOSError):
    status_code = 503
    error_code = "database_operation_error"


class NotFoundError(CareerOSError):
    status_code = 404
    error_code = "not_found"


class AuthenticationError(CareerOSError):
    status_code = 401
    error_code = "authentication_failed"


class AuthorizationError(CareerOSError):
    status_code = 403
    error_code = "authorization_failed"


class ConflictError(CareerOSError):
    status_code = 409
    error_code = "conflict"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CareerOSError)
    async def handle_careeros_error(_: Request, exc: CareerOSError) -> JSONResponse:
        logger.warning("request_failed", extra={"error_code": exc.error_code, "error_message": exc.message})
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.error_code, "message": exc.message}},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unexpected_error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "internal_error", "message": "Unexpected server error."}},
        )
