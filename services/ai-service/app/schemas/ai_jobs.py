from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AIJobCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job_type: str
    input_reference: str | None = None


class AIJobCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: str
    status: str
    created_at: datetime


class AIJobStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: str
    status: str
    result: str | None = None
    error: str | None = None