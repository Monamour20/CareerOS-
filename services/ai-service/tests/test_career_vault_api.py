from app.api.dependencies import get_career_profile_vault_service, get_current_user
from app.core.errors import NotFoundError
from app.domain.career_profile.models import CareerProfile
from app.infrastructure.database.models import UserRecord
from app.main import app
from tests.conftest import VALID_PROFILE


class FakeCareerProfileVaultService:
    def __init__(self):
        self.profile = CareerProfile.model_validate(VALID_PROFILE)

    def save(self, profile: CareerProfile, user_id: int | None = None) -> int:
        self.profile = profile
        return user_id or 42

    def get(self, user_id: int) -> CareerProfile:
        if user_id != 42:
            raise NotFoundError("CareerProfile was not found for the requested user.")
        return self.profile


def fake_current_user() -> UserRecord:
    return UserRecord(id=42, email="ada@example.com", full_name="Ada Lovelace")


def test_create_career_profile_endpoint(client):
    app.dependency_overrides[get_career_profile_vault_service] = (
        lambda: FakeCareerProfileVaultService()
    )
    app.dependency_overrides[get_current_user] = fake_current_user

    response = client.post(
        "/api/v1/career-profile",
        json={"career_profile": VALID_PROFILE},
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == 42
    assert response.json()["career_profile"]["personal_information"]["full_name"] == "Ada Lovelace"


def test_get_career_profile_endpoint(client):
    app.dependency_overrides[get_career_profile_vault_service] = (
        lambda: FakeCareerProfileVaultService()
    )
    app.dependency_overrides[get_current_user] = fake_current_user

    response = client.get("/api/v1/career-profile/42")

    assert response.status_code == 200
    assert response.json()["career_profile"]["skills"]["technical"] == ["Python"]


def test_get_career_profile_rejects_other_users(client):
    app.dependency_overrides[get_career_profile_vault_service] = (
        lambda: FakeCareerProfileVaultService()
    )
    app.dependency_overrides[get_current_user] = fake_current_user

    response = client.get("/api/v1/career-profile/7")

    assert response.status_code == 403
