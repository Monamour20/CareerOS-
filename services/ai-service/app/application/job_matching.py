from __future__ import annotations

import re

from app.domain.career_profile.models import CareerProfile
from app.domain.job.models import Job, JobMatch


class JobMatchingService:
    """Deterministic, explainable matching between a CareerProfile and Job."""

    ROLE_WEIGHT = 25.0
    SKILL_WEIGHT = 45.0
    SENIORITY_WEIGHT = 10.0
    INDUSTRY_WEIGHT = 10.0
    EXPERIENCE_WEIGHT = 10.0

    def match(
        self,
        *,
        job_id: int,
        job: Job,
        profile: CareerProfile,
    ) -> JobMatch:
        profile_skills = self._collect_profile_skills(profile)

        required_job_skills = {
            self._normalize_skill(skill.name)
            for skill in job.skills
            if skill.name.strip() and skill.required
        }

        optional_job_skills = {
            self._normalize_skill(skill.name)
            for skill in job.skills
            if skill.name.strip() and not skill.required
        }

        all_job_skills = required_job_skills | optional_job_skills

        matched_required = sorted(
            skill
            for skill in required_job_skills
            if self._skill_matches(skill, profile_skills)
        )

        matched_optional = sorted(
            skill
            for skill in optional_job_skills
            if self._skill_matches(skill, profile_skills)
        )

        matched_skills = sorted(
            set(matched_required) | set(matched_optional)
        )

        missing_required = sorted(
            skill
            for skill in required_job_skills
            if skill not in matched_required
        )

        missing_optional = sorted(
            skill
            for skill in optional_job_skills
            if skill not in matched_optional
        )

        missing_skills = sorted(
            set(missing_required) | set(missing_optional)
        )

        skill_score = self._skill_score(
            required_skills=required_job_skills,
            optional_skills=optional_job_skills,
            matched_required=matched_required,
            matched_optional=matched_optional,
        )

        role_score = self._role_score(
            job_title=job.title,
            target_roles=profile.career_interests.target_roles,
        )

        seniority_score = self._seniority_score(
            job_seniority=job.seniority,
            profile_seniority=profile.career_interests.seniority,
        )

        industry_score = self._industry_score(
            job=job,
            industries=profile.career_interests.industries,
        )

        experience_score = self._experience_score(
            job=job,
            profile=profile,
        )

        score = (
            skill_score * self.SKILL_WEIGHT
            + role_score * self.ROLE_WEIGHT
            + seniority_score * self.SENIORITY_WEIGHT
            + industry_score * self.INDUSTRY_WEIGHT
            + experience_score * self.EXPERIENCE_WEIGHT
        )

        # A job missing required skills should never look like a perfect match.
        if required_job_skills:
            required_match_ratio = (
                len(matched_required) / len(required_job_skills)
            )

            if required_match_ratio < 0.5:
                score *= 0.75

        reasons = self._build_reasons(
            matched_required=matched_required,
            matched_optional=matched_optional,
            missing_required=missing_required,
            missing_optional=missing_optional,
            role_score=role_score,
            seniority_score=seniority_score,
            industry_score=industry_score,
            experience_score=experience_score,
        )

        return JobMatch(
            job_id=job_id,
            score=round(max(0.0, min(score, 100.0)), 2),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            reasons=reasons,
        )

    def _collect_profile_skills(
        self,
        profile: CareerProfile,
    ) -> set[str]:
        skills: set[str] = set()

        for values in (
            profile.skills.technical,
            profile.skills.tools,
            profile.skills.languages,
        ):
            skills.update(
                self._normalize_skill(value)
                for value in values
                if value.strip()
            )

        for experience in profile.experience:
            skills.update(
                self._normalize_skill(value)
                for value in experience.technologies
                if value.strip()
            )

        for project in profile.projects:
            skills.update(
                self._normalize_skill(value)
                for value in project.technologies
                if value.strip()
            )

        return {
            skill
            for skill in skills
            if skill
        }

    def _skill_matches(
        self,
        job_skill: str,
        profile_skills: set[str],
    ) -> bool:
        if job_skill in profile_skills:
            return True

        for profile_skill in profile_skills:
            if self._related_skill(job_skill, profile_skill):
                return True

        return False

    @staticmethod
    def _related_skill(
        first: str,
        second: str,
    ) -> bool:
        aliases = {
            "javascript": {
                "javascript",
                "js",
            },
            "typescript": {
                "typescript",
                "ts",
            },
            "react": {
                "react",
                "reactjs",
                "react.js",
            },
            "nextjs": {
                "nextjs",
                "next.js",
            },
            "nodejs": {
                "nodejs",
                "node.js",
            },
            "postgresql": {
                "postgresql",
                "postgres",
            },
            "machine learning": {
                "machine learning",
                "ml",
            },
            "artificial intelligence": {
                "artificial intelligence",
                "ai",
            },
            "generative ai": {
                "generative ai",
                "genai",
            },
        }

        for values in aliases.values():
            if first in values and second in values:
                return True

        return False

    def _skill_score(
        self,
        *,
        required_skills: set[str],
        optional_skills: set[str],
        matched_required: list[str],
        matched_optional: list[str],
    ) -> float:
        required_score = (
            len(matched_required) / len(required_skills)
            if required_skills
            else 1.0
        )

        optional_score = (
            len(matched_optional) / len(optional_skills)
            if optional_skills
            else 1.0
        )

        if required_skills and optional_skills:
            return (
                required_score * 0.8
                + optional_score * 0.2
            )

        if required_skills:
            return required_score

        if optional_skills:
            return optional_score

        # No extracted skills should not give the job a free 50% score.
        return 0.0

    def _role_score(
        self,
        *,
        job_title: str,
        target_roles: list[str],
    ) -> float:
        if not target_roles:
            return 0.0

        title = self._normalize_text(job_title)
        best_score = 0.0

        role_aliases = {
            "machine learning engineer": {
                "machine learning engineer",
                "ml engineer",
                "machine learning developer",
            },
            "ai engineer": {
                "ai engineer",
                "artificial intelligence engineer",
                "ai developer",
            },
            "software engineer": {
                "software engineer",
                "software developer",
                "software development engineer",
                "sde",
            },
            "data scientist": {
                "data scientist",
                "data science engineer",
            },
        }

        for role in target_roles:
            normalized_role = self._normalize_text(role)

            if not normalized_role:
                continue

            if normalized_role == title:
                best_score = max(best_score, 1.0)
                continue

            aliases = role_aliases.get(
                normalized_role,
                {normalized_role},
            )

            if title in aliases or any(
                alias in title
                for alias in aliases
            ):
                best_score = max(best_score, 0.95)
                continue

            if normalized_role in title or title in normalized_role:
                best_score = max(best_score, 0.85)
                continue

            role_words = set(normalized_role.split())
            title_words = set(title.split())

            if role_words and role_words.intersection(title_words):
                best_score = max(best_score, 0.5)

        return best_score

    def _seniority_score(
        self,
        *,
        job_seniority: str | None,
        profile_seniority: str | None,
    ) -> float:
        if not job_seniority or not profile_seniority:
            return 0.5

        job_level = self._seniority_level(job_seniority)
        profile_level = self._seniority_level(profile_seniority)

        if job_level is None or profile_level is None:
            return 0.5

        difference = abs(job_level - profile_level)

        if difference == 0:
            return 1.0

        if difference == 1:
            return 0.5

        return 0.0

    @staticmethod
    def _seniority_level(
        value: str,
    ) -> int | None:
        normalized = value.lower()

        levels = (
            ("intern", 0),
            ("trainee", 0),
            ("entry", 1),
            ("junior", 1),
            ("associate", 2),
            ("mid", 2),
            ("intermediate", 2),
            ("senior", 3),
            ("lead", 4),
            ("principal", 5),
            ("staff", 5),
            ("manager", 5),
            ("director", 6),
        )

        for keyword, level in levels:
            if keyword in normalized:
                return level

        return None

    def _industry_score(
        self,
        *,
        job: Job,
        industries: list[str],
    ) -> float:
        if not industries:
            return 0.0

        searchable_text = self._normalize_text(
            f"{job.title} {job.description} {job.company}"
        )

        best_score = 0.0

        industry_aliases = {
            "artificial intelligence": {
                "artificial intelligence",
                "ai",
                "machine learning",
                "deep learning",
                "generative ai",
            },
            "technology": {
                "technology",
                "software",
                "saas",
                "information technology",
            },
            "software": {
                "software",
                "software development",
                "technology",
            },
        }

        for industry in industries:
            normalized_industry = self._normalize_text(industry)

            if not normalized_industry:
                continue

            aliases = industry_aliases.get(
                normalized_industry,
                {normalized_industry},
            )

            for alias in aliases:
                if alias in searchable_text:
                    best_score = max(best_score, 1.0)

        return best_score

    def _experience_score(
        self,
        *,
        job: Job,
        profile: CareerProfile,
    ) -> float:
        if not profile.experience:
            return 0.5

        job_text = self._normalize_text(
            f"{job.title} {job.description}"
        )

        experience_terms: set[str] = set()

        for experience in profile.experience:
            if experience.title:
                experience_terms.update(
                    self._normalize_text(
                        experience.title
                    ).split()
                )

            for technology in experience.technologies:
                normalized = self._normalize_text(technology)

                if normalized:
                    experience_terms.add(normalized)

        if not experience_terms:
            return 0.5

        matches = sum(
            1
            for term in experience_terms
            if term in job_text
        )

        return min(
            1.0,
            matches / max(len(experience_terms), 1),
        )

    @staticmethod
    def _build_reasons(
        *,
        matched_required: list[str],
        matched_optional: list[str],
        missing_required: list[str],
        missing_optional: list[str],
        role_score: float,
        seniority_score: float,
        industry_score: float,
        experience_score: float,
    ) -> list[str]:
        reasons: list[str] = []

        if matched_required:
            reasons.append(
                f"Matches {len(matched_required)} required skill(s)."
            )

        if matched_optional:
            reasons.append(
                f"Matches {len(matched_optional)} optional skill(s)."
            )

        if missing_required:
            reasons.append(
                f"Missing {len(missing_required)} required skill(s): "
                f"{', '.join(missing_required)}."
            )

        if missing_optional:
            reasons.append(
                f"Missing {len(missing_optional)} optional skill(s)."
            )

        if role_score >= 0.95:
            reasons.append(
                "The role closely matches a target career role."
            )
        elif role_score >= 0.5:
            reasons.append(
                "The role has some overlap with a target career role."
            )

        if seniority_score == 1.0:
            reasons.append(
                "The job seniority matches the preferred seniority."
            )
        elif seniority_score == 0.5:
            reasons.append(
                "The job seniority is close to the preferred level."
            )
        elif seniority_score == 0.0:
            reasons.append(
                "The job seniority differs from the preferred level."
            )

        if industry_score == 1.0:
            reasons.append(
                "The job appears related to a preferred industry."
            )

        if experience_score >= 0.8:
            reasons.append(
                "The role aligns well with previous experience."
            )
        elif experience_score >= 0.5:
            reasons.append(
                "The role has some overlap with previous experience."
            )

        if not reasons:
            reasons.append(
                "Limited matching evidence was found in the Career Vault."
            )

        return reasons

    @staticmethod
    def _normalize_skill(
        value: str,
    ) -> str:
        normalized = value.lower().strip()

        normalized = normalized.replace(
            "react.js",
            "react",
        )

        normalized = normalized.replace(
            "reactjs",
            "react",
        )

        normalized = normalized.replace(
            "next.js",
            "nextjs",
        )

        normalized = normalized.replace(
            "node.js",
            "nodejs",
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        normalized = value.lower().strip()

        normalized = re.sub(
            r"[^a-z0-9+#.\s-]",
            " ",
            normalized,
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized