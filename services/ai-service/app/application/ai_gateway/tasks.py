from enum import StrEnum


class AITask(StrEnum):
    CAREER_PROFILE_EXTRACTION = "career_profile_extraction"
    JOB_DISCOVERY = "job_discovery"
    JOB_EVALUATION = "job_evaluation"
    JOB_MATCHING = "job_matching"
    APPLICATION_WRITING = "application_writing"
    APPLICATION_REVIEW = "application_review"
    AGENT_PLANNING = "agent_planning"