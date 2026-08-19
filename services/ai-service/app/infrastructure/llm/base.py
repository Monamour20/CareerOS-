from typing import Protocol


class LLMClient(Protocol):
    async def analyze_resume(self, resume_text: str) -> str:
        """Return structured CareerProfile JSON as text."""
