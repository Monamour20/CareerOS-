from pathlib import Path

import httpx

from app.core.errors import (
    InvalidLLMOutputError,
    LLMConnectionError,
    LLMTimeoutError,
)


class OllamaProvider:
    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: float,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

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

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "think": False,
            "keep_alive": "10m",
            "options": {
                "temperature": 0.1,
                "top_k": 20,
                "top_p": 0.9,
                "num_ctx": 4096,
                "num_predict": 1800,
            },
        }

        try:
            timeout = httpx.Timeout(
                connect=10.0,
                read=self.timeout_seconds,
                write=30.0,
                pool=30.0,
            )

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )

                response.raise_for_status()

        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(
                "Ollama request timed out while analyzing the resume."
            ) from exc

        except httpx.HTTPError as exc:
            raise LLMConnectionError(
                "Could not connect to Ollama or Ollama returned an error."
            ) from exc

        data = response.json()

        result = data.get("response")

        if not isinstance(result, str) or not result.strip():
            raise InvalidLLMOutputError(
                "Ollama returned an empty response."
            )

        return result