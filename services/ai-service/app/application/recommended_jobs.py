from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.application.job_matching import JobMatchingService
from app.application.jobs import JobService
from app.domain.career_profile.models import CareerProfile
from app.domain.job.models import Job, JobMatch
from app.infrastructure.database.repositories.job import job_to_domain


class RecommendationCategory(str, Enum):
    EXCELLENT = "excellent"
    STRONG = "strong"
    POTENTIAL = "potential"
    SKILL_GAP = "skill_gap"


@dataclass(frozen=True)
class RecommendedJob:
    job_id: int
    match: JobMatch
    category: RecommendationCategory


class RecommendedJobsService:
    """Build explainable job recommendations from the Career Vault."""

    MIN_RECOMMENDATION_SCORE = 40.0
    MAX_CANDIDATES = 100

    EXCELLENT_SCORE = 85.0
    STRONG_SCORE = 70.0
    POTENTIAL_SCORE = 40.0

    def __init__(
        self,
        *,
        job_service: JobService,
        matching_service: JobMatchingService,
    ):
        self.job_service = job_service
        self.matching_service = matching_service

    def recommend(
        self,
        *,
        profile: CareerProfile,
        limit: int = 20,
        offset: int = 0,
    ) -> list[RecommendedJob]:
        if limit < 1:
            return []

        if offset < 0:
            offset = 0

        records = self.job_service.list_jobs(
            limit=self.MAX_CANDIDATES,
            offset=0,
        )

        ranked: list[RecommendedJob] = []

        for record in records:
            job = job_to_domain(record)

            match = self.matching_service.match(
                job_id=record.id,
                job=job,
                profile=profile,
            )

            category = self._classify_match(
                job=job,
                match=match,
            )

            if not self._is_relevant_match(
                job=job,
                match=match,
                category=category,
            ):
                continue

            ranked.append(
                RecommendedJob(
                    job_id=record.id,
                    match=match,
                    category=category,
                )
            )

        ranked.sort(
            key=self._ranking_key,
            reverse=True,
        )

        return ranked[offset : offset + limit]

    @classmethod
    def _classify_match(
        cls,
        *,
        job: Job,
        match: JobMatch,
    ) -> RecommendationCategory:
        required_skill_count = cls._required_skill_count(job)
        missing_required_count = cls._missing_required_skill_count(
            job=job,
            match=match,
        )

        if (
            required_skill_count > 0
            and missing_required_count > 0
        ):
            return RecommendationCategory.SKILL_GAP

        if match.score >= cls.EXCELLENT_SCORE:
            return RecommendationCategory.EXCELLENT

        if match.score >= cls.STRONG_SCORE:
            return RecommendationCategory.STRONG

        return RecommendationCategory.POTENTIAL

    @classmethod
    def _is_relevant_match(
        cls,
        *,
        job: Job,
        match: JobMatch,
        category: RecommendationCategory,
    ) -> bool:
        if match.score < cls.MIN_RECOMMENDATION_SCORE:
            return False

        required_skill_count = cls._required_skill_count(job)

        if required_skill_count == 0:
            return True

        missing_required_count = cls._missing_required_skill_count(
            job=job,
            match=match,
        )

        required_match_ratio = (
            (required_skill_count - missing_required_count)
            / required_skill_count
        )

        # Do not recommend a job when less than half of its
        # required skills are matched.
        if required_match_ratio < 0.5:
            return False

        # A job with a real skill gap can still be useful when
        # most required skills are already present.
        return category != RecommendationCategory.SKILL_GAP or (
            required_match_ratio >= 0.5
        )

    @staticmethod
    def _required_skill_count(job: Job) -> int:
        return sum(
            1
            for skill in job.skills
            if skill.required and skill.name.strip()
        )

    @staticmethod
    def _missing_required_skill_count(
        *,
        job: Job,
        match: JobMatch,
    ) -> int:
        required_skill_names = {
            skill.name.strip().lower()
            for skill in job.skills
            if skill.required and skill.name.strip()
        }

        missing_skills = {
            skill.strip().lower()
            for skill in match.missing_skills
            if skill.strip()
        }

        return len(required_skill_names.intersection(missing_skills))

    @staticmethod
    def _ranking_key(
        recommendation: RecommendedJob,
    ) -> tuple[float, float, float]:
        category_priority = {
            RecommendationCategory.EXCELLENT: 4.0,
            RecommendationCategory.STRONG: 3.0,
            RecommendationCategory.POTENTIAL: 2.0,
            RecommendationCategory.SKILL_GAP: 1.0,
        }

        return (
            category_priority[recommendation.category],
            recommendation.match.score,
            float(len(recommendation.match.matched_skills)),
        )