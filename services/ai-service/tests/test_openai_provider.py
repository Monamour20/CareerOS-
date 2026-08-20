import json

import pytest

from app.domain.career_profile.models import CareerProfile
from app.infrastructure.llm.openai import OpenAIProvider


class FakeParsedResponse:
    def __init__(self, profile: CareerProfile):
        self.output_parsed = profile


class FakeResponses:
    def __init__(self, profile: CareerProfile):
        self.profile = profile
        self.received_model = None
        self.received_input = None
        self.received_text_format = None

    async def parse(self, *, model, input, text_format):
        self.received_model = model
        self.received_input = input
        self.received_text_format = text_format

        return FakeParsedResponse(self.profile)


class FakeOpenAIClient:
    def __init__(self, profile: CareerProfile):
        self.responses = FakeResponses(profile)


@pytest.mark.asyncio
async def test_openai_provider_returns_career_profile_json(tmp_path):
    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        timeout_seconds=30,
    )

    profile = CareerProfile()
    provider.client = FakeOpenAIClient(profile)

    result = await provider.analyze_resume(
        "Ada Lovelace\nPython\nAnalytical Engine"
    )

    parsed = json.loads(result)

    assert parsed["personal_information"]["full_name"] is None
    assert parsed["skills"]["technical"] == []


@pytest.mark.asyncio
async def test_openai_provider_uses_career_profile_schema():
    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        timeout_seconds=30,
    )

    profile = CareerProfile()
    fake_client = FakeOpenAIClient(profile)
    provider.client = fake_client

    await provider.analyze_resume("Ada Lovelace")

    assert fake_client.responses.received_model == "test-model"
    assert fake_client.responses.received_text_format is CareerProfile
    assert "Ada Lovelace" in fake_client.responses.received_input