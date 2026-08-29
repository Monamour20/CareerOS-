from app.application.ai_gateway import AIGateway, AIRequest, AITask
from app.application.career_intelligence.context import CareerContext


class CareerIntelligenceService:
    """Builds and analyzes a user's career context."""

    def __init__(self, ai_gateway: AIGateway):
        self.ai_gateway = ai_gateway

    def build_context(
        self,
        *,
        summary: str = "",
        skills: list[str] | None = None,
        experiences: list[str] | None = None,
        education: list[str] | None = None,
        projects: list[str] | None = None,
        certifications: list[str] | None = None,
        preferences: list[str] | None = None,
    ) -> CareerContext:
        return CareerContext(
            summary=summary.strip(),
            skills=tuple(self._clean(skills)),
            experiences=tuple(self._clean(experiences)),
            education=tuple(self._clean(education)),
            projects=tuple(self._clean(projects)),
            certifications=tuple(self._clean(certifications)),
            preferences=tuple(self._clean(preferences)),
        )

    async def analyze(
        self,
        context: CareerContext,
    ) -> str:
        return await self.ai_gateway.execute(
            AIRequest(
                task=AITask.CAREER_PROFILE_EXTRACTION,
                system_prompt=(
                    "You are CareerOS Career Intelligence. "
                    "Analyze career information accurately. "
                    "Never invent experience, skills, education, "
                    "or preferences."
                ),
                user_prompt=(
                    "Analyze the following career context and "
                    "return useful structured career insights.\n\n"
                    f"{context.to_prompt_context()}"
                ),
            )
        )

    @staticmethod
    def _clean(values: list[str] | None) -> list[str]:
        if not values:
            return []

        return [
            value.strip()
            for value in values
            if isinstance(value, str) and value.strip()
        ]