from app.application.ai_gateway import AIGateway, AIRequest, AITask
from app.application.career_intelligence.context import CareerContext
from app.application.career_intelligence.models import CareerAnalysis


class CareerIntelligenceService:
    """Analyzes a user's career context into actionable career insights."""

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
    ) -> CareerAnalysis:
        raw_output = await self.ai_gateway.execute(
            AIRequest(
                task=AITask.CAREER_PROFILE_EXTRACTION,
                system_prompt=(
                    "You are CareerOS Career Intelligence. "
                    "Analyze the user's career information accurately. "
                    "Never invent experience, skills, education, "
                    "achievements, or preferences. "
                    "Return ONLY valid JSON. "
                    "Do not use Markdown code fences."
                ),
                user_prompt=(
                    "Analyze the following career context and produce "
                    "actionable career intelligence.\n\n"
                    f"{context.to_prompt_context()}\n\n"
                    "Return JSON with exactly these fields:\n"
                    "- career_summary: string\n"
                    "- strengths: array of strings\n"
                    "- growth_areas: array of strings\n"
                    "- next_actions: array of strings"
                ),
            )
        )

        return CareerAnalysis.model_validate_json(
            self._clean_json_output(raw_output)
        )

    @staticmethod
    def _clean_json_output(raw_output: str) -> str:
        """Remove accidental Markdown code fences around JSON."""

        output = raw_output.strip()

        if output.startswith("```json"):
            output = output[len("```json"):].strip()
        elif output.startswith("```"):
            output = output[len("```"):].strip()

        if output.endswith("```"):
            output = output[:-3].strip()

        return output

    @staticmethod
    def _clean(values: list[str] | None) -> list[str]:
        if not values:
            return []

        return [
            value.strip()
            for value in values
            if isinstance(value, str) and value.strip()
        ]