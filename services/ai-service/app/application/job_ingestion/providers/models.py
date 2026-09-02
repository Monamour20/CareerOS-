from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class JobSearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    remote: bool | None = None
    limit: int = Field(default=25, ge=1, le=100)


class JobProviderResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    jobs: list[dict]
    total: int | None = None