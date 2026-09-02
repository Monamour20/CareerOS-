from pydantic import BaseModel, ConfigDict, Field


class CareerAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    career_summary: str = ""
    strengths: list[str] = Field(default_factory=list)
    growth_areas: list[str] = Field(default_factory=list)
    recommended_roles: list[str] = Field(default_factory=list)
    recommended_industries: list[str] = Field(default_factory=list)
    skill_gaps: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
