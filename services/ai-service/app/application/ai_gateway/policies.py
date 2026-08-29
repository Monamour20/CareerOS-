from dataclasses import dataclass

from app.application.ai_gateway.tasks import AITask


@dataclass(frozen=True)
class AIRoutingPolicy:
    capability: str
    preferred_provider: str


DEFAULT_ROUTING_POLICIES: dict[AITask, AIRoutingPolicy] = {
    AITask.CAREER_PROFILE_EXTRACTION: AIRoutingPolicy(
        capability="structured_extraction",
        preferred_provider="ollama",
    ),
    AITask.JOB_DISCOVERY: AIRoutingPolicy(
        capability="fast_reasoning",
        preferred_provider="ollama",
    ),
    AITask.JOB_EVALUATION: AIRoutingPolicy(
        capability="reasoning",
        preferred_provider="ollama",
    ),
    AITask.JOB_MATCHING: AIRoutingPolicy(
        capability="deep_reasoning",
        preferred_provider="ollama",
    ),
    AITask.APPLICATION_WRITING: AIRoutingPolicy(
        capability="high_quality_writing",
        preferred_provider="ollama",
    ),
    AITask.APPLICATION_REVIEW: AIRoutingPolicy(
        capability="deep_reasoning",
        preferred_provider="ollama",
    ),
    AITask.AGENT_PLANNING: AIRoutingPolicy(
        capability="agentic_reasoning",
        preferred_provider="ollama",
    ),
}