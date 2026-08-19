from pydantic import BaseModel, Field

from app.domain.career_profile.models import CareerProfile


class PlaceholderRequest(BaseModel):
    """Multipart uploads are represented by FastAPI's UploadFile."""


class CareerProfileCreateRequest(BaseModel):
    user_id: int | None = None
    career_profile: CareerProfile


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=128)


class OnboardingCareerProfileRequest(BaseModel):
    career_status: str | None = Field(default=None, max_length=64)
    preferred_work_mode: str | None = Field(default=None, max_length=64)
    career_goals: str | None = Field(default=None, max_length=2000)
    resume_creation_requested: bool = False
    career_profile: CareerProfile
