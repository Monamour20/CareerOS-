from dataclasses import dataclass

from app.application.ai_gateway.tasks import AITask
from app.infrastructure.llm.base import LLMClient


@dataclass(frozen=True)
class AIRequest:
    task: AITask
    system_prompt: str
    user_prompt: str


class AIGateway:
    """Coordinates AI tasks without coupling CareerOS to a specific model."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def execute(self, request: AIRequest) -> str:
        if request.task == AITask.CAREER_PROFILE_EXTRACTION:
            return await self.llm_client.generate(
                system_prompt=request.system_prompt,
                user_prompt=request.user_prompt,
            )

        return await self.llm_client.generate(
            system_prompt=request.system_prompt,
            user_prompt=request.user_prompt,
        )