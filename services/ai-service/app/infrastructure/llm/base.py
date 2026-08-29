from typing import Protocol


class LLMClient(Protocol):
    async def analyze_resume(self, resume_text: str) -> str:
        """Extract a validated CareerProfile from resume text."""

    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """Generate a general-purpose AI response."""