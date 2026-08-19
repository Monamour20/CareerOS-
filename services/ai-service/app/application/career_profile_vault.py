from app.core.errors import NotFoundError
from app.domain.career_profile.models import CareerProfile
from app.infrastructure.database.repositories.career_profile import CareerProfileRepository


class CareerProfileVaultService:
    def __init__(self, repository: CareerProfileRepository):
        self.repository = repository

    def save(self, profile: CareerProfile, user_id: int | None = None) -> int:
        validated_profile = CareerProfile.model_validate(profile)
        return self.repository.save(validated_profile, user_id=user_id)

    def get(self, user_id: int) -> CareerProfile:
        profile = self.repository.get_by_user_id(user_id)
        if profile is None:
            raise NotFoundError("CareerProfile was not found for the requested user.")
        return profile
