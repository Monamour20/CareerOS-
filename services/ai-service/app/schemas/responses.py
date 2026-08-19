from pydantic import BaseModel

from app.domain.career_profile.models import CareerProfile


class ResumeAnalysisResponse(BaseModel):
    career_profile: CareerProfile


class StoredCareerProfileResponse(BaseModel):
    user_id: int
    career_profile: CareerProfile


class UserResponse(BaseModel):
    id: int
    full_name: str | None = None
    email: str | None = None
    account_type: str | None = None
    career_status: str | None = None
    preferred_work_mode: str | None = None
    career_goals: str | None = None
    onboarding_completed: bool = False
    resume_creation_requested: bool = False


class AuthResponse(BaseModel):
    token: str
    expires_at: str
    user: UserResponse
