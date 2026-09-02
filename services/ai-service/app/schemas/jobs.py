from pydantic import BaseModel, ConfigDict, Field


class JobSkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    required: bool


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str | None
    source: str
    title: str
    company: str
    location: str | None
    remote: bool
    employment_type: str | None
    seniority: str | None
    description: str
    application_url: str | None
    salary_min: float | None
    salary_max: float | None
    currency: str | None
    posted_at: str | None
    expires_at: str | None
    skills: list[JobSkillResponse] = Field(
        default_factory=list
    )


class JobListResponse(BaseModel):
    jobs: list[JobResponse]
    limit: int
    offset: int


class JobDiscoveryResponse(BaseModel):
    source: str
    discovered: int
    created: int
    updated: int
    jobs: list[JobResponse]


class JobMatchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job: JobResponse
    score: float = Field(ge=0, le=100)
    category: str
    matched_skills: list[str] = Field(
        default_factory=list
    )
    missing_skills: list[str] = Field(
        default_factory=list
    )
    reasons: list[str] = Field(
        default_factory=list
    )