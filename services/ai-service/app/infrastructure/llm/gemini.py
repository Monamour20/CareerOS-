from pathlib import Path

from google import genai
from google.genai import types

from app.core.errors import (
    InvalidLLMOutputError,
    LLMConnectionError,
    LLMTimeoutError,
)
from app.domain.career_profile.models import CareerProfile


class GeminiProvider:
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ):
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.client = genai.Client(api_key=api_key)

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
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )

        except TimeoutError as exc:
            raise LLMTimeoutError(
                "Gemini request timed out while analyzing the resume."
            ) from exc

        except Exception as exc:
            raise LLMConnectionError(
                "Could not connect to Gemini or Gemini returned an error."
            ) from exc

        if not response.text:
            raise InvalidLLMOutputError(
                "Gemini returned an empty response."
            )

        try:
            profile = CareerProfile.model_validate_json(response.text)
        except Exception as exc:
            raise InvalidLLMOutputError(
                "Gemini returned an invalid CareerProfile response."
            ) from exc

        return profile.model_dump_json()

    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        prompt = (
            f"SYSTEM INSTRUCTIONS:\n"
            f"{system_prompt}\n\n"
            f"USER REQUEST:\n"
            f"{user_prompt}"
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                ),
            )

        except TimeoutError as exc:
            raise LLMTimeoutError(
                "Gemini request timed out while generating career intelligence."
            ) from exc

        except Exception as exc:
            raise LLMConnectionError(
                "Could not connect to Gemini or Gemini returned an error."
            ) from exc

        if not response.text:
            raise InvalidLLMOutputError(
                "Gemini returned an empty response."
            )

        return response.text.strip()
