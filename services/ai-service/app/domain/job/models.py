from pydantic import BaseModel, ConfigDict, Field


class JobSkill(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    required: bool = True


class Job(BaseModel):
    model_config = ConfigDict(extra="forbid")

    external_id: str | None = None
    source: str
    title: str
    company: str
    location: str | None = None
    remote: bool = False
    employment_type: str | None = None
    seniority: str | None = None
    description: str = ""
    application_url: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    currency: str | None = None
    posted_at: str | None = None
    expires_at: str | None = None
    skills: list[JobSkill] = Field(default_factory=list)


class JobMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job_id: int
    score: float = Field(ge=0, le=100)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)