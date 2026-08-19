from app.application.career_profile_vault import CareerProfileVaultService
from app.domain.career_profile.models import CareerProfile
from app.infrastructure.database.models import UserRecord
from app.infrastructure.database.repositories.account import AccountRepository


class OnboardingService:
    def __init__(
        self,
        account_repository: AccountRepository,
        vault_service: CareerProfileVaultService,
    ):
        self.account_repository = account_repository
        self.vault_service = vault_service

    def complete(
        self,
        user: UserRecord,
        *,
        career_status: str | None,
        preferred_work_mode: str | None,
        career_goals: str | None,
        resume_creation_requested: bool,
        career_profile: CareerProfile,
    ) -> int:
        validated_profile = CareerProfile.model_validate(career_profile)
        user_id = self.vault_service.save(validated_profile, user_id=user.id)
        self.account_repository.update_onboarding(
            user,
            career_status=career_status,
            preferred_work_mode=preferred_work_mode,
            career_goals=career_goals,
            resume_creation_requested=resume_creation_requested,
        )
        return user_id
