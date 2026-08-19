import pytest

from app.core.errors import InvalidLLMOutputError
from app.domain.career_profile.validator import CareerProfileValidator
from tests.conftest import VALID_PROFILE


def test_career_profile_validation_accepts_valid_profile():
    profile = CareerProfileValidator().validate(VALID_PROFILE)

    assert profile.personal_information.full_name == "Ada Lovelace"


def test_career_profile_validation_repairs_markdown_json():
    output = f"```json\n{CareerProfileValidator().validate(VALID_PROFILE).model_dump_json()}\n```"

    profile = CareerProfileValidator().validate(output)

    assert profile.skills.technical == ["Python"]


def test_invalid_llm_output():
    with pytest.raises(InvalidLLMOutputError):
        CareerProfileValidator().validate("not json")


def test_career_profile_validation_repairs_extra_keys():
    invalid = dict(VALID_PROFILE)
    invalid["unexpected"] = True

    profile = CareerProfileValidator().validate(invalid)

    assert profile.personal_information.full_name == "Ada Lovelace"
