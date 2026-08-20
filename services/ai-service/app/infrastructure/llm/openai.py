from pathlib import Path

from openai import AsyncOpenAI

from app.core.errors import (
    InvalidLLMOutputError,
    LLMConnectionError,
    LLMTimeoutError,
)
from app.domain.career_profile.models import CareerProfile


class OpenAIProvider:
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ):
        self.model = model
        self.timeout_seconds = timeout_seconds

        self.client = AsyncOpenAI(
            api_key=api_key,
            timeout=timeout_seconds,
        )

        self.prompt_template = (
            Path(__file__).parent
            / "prompts"
            / "resume_analysis.md"
        ).read_text(encoding="utf-8")

    async def analyze_resume(self, resume_text: str) -> str:
        prompt = self.prompt_template.replace(
            "{{RESUME_TEXT}}",
            resume_text,
        )

        try:
            response = await self.client.responses.parse(
                model=self.model,
                input=prompt,
                text_format=CareerProfile,
            )

        except TimeoutError as exc:
            raise LLMTimeoutError(
                "OpenAI request timed out while analyzing the resume."
            ) from exc

        except Exception as exc:
            raise LLMConnectionError(
                "Could not connect to OpenAI or OpenAI returned an error."
            ) from exc

        profile = response.output_parsed

        if not isinstance(profile, CareerProfile):
            raise InvalidLLMOutputError(
                "OpenAI returned an invalid CareerProfile response."
            )

        return profile.model_dump_json()