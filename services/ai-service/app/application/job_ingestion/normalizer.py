from __future__ import annotations

import re
from typing import Any

from app.domain.job.models import Job, JobSkill


class JobNormalizer:
    """Converts provider-specific job data into the CareerOS Job model."""

    COMMON_SKILLS = {
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "next.js",
        "node.js",
        "fastapi",
        "django",
        "flask",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "github",
        "linux",
        "terraform",
        "pytorch",
        "tensorflow",
        "scikit-learn",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "generative ai",
        "llm",
        "data science",
        "data analysis",
        "power bi",
        "tableau",
        "excel",
        "spark",
    }

    def normalize(
        self,
        *,
        source: str,
        data: dict[str, Any],
    ) -> Job:
        if source == "adzuna":
            data = self._normalize_adzuna(data)

        title = self._required_string(data, "title")
        company = self._required_string(data, "company")

        description = self._string(data.get("description")) or ""

        skills = self._extract_skills(
            description,
            data.get("skills"),
        )

        return Job(
            external_id=self._string(data.get("external_id")),
            source=source,
            title=title,
            company=company,
            location=self._string(data.get("location")),
            remote=self._to_bool(data.get("remote")),
            employment_type=self._string(data.get("employment_type")),
            seniority=self._string(data.get("seniority")),
            description=description,
            application_url=self._string(data.get("application_url")),
            salary_min=self._to_float(data.get("salary_min")),
            salary_max=self._to_float(data.get("salary_max")),
            currency=self._string(data.get("currency")),
            posted_at=self._string(data.get("posted_at")),
            expires_at=self._string(data.get("expires_at")),
            skills=skills,
        )

    def _normalize_adzuna(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert an Adzuna job response into the generic CareerOS
        job structure expected by the normalizer.
        """

        company_data = data.get("company")
        location_data = data.get("location")

        company = None

        if isinstance(company_data, dict):
            company = company_data.get("display_name")

        location = None

        if isinstance(location_data, dict):
            location = location_data.get("display_name")

        salary_min = data.get("salary_min")
        salary_max = data.get("salary_max")

        return {
            "external_id": (
                str(data["id"])
                if data.get("id") is not None
                else None
            ),
            "title": data.get("title"),
            "company": company,
            "location": location,
            "remote": self._adzuna_is_remote(data),
            "employment_type": None,
            "seniority": None,
            "description": data.get("description"),
            "application_url": data.get("redirect_url"),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "currency": self._string(
                data.get("salary_currency")
            ),
            "posted_at": data.get("created"),
            "expires_at": data.get("expiration_date"),
            "skills": [],
        }

    @staticmethod
    def _adzuna_is_remote(
        data: dict[str, Any],
    ) -> bool:
        """Detect remote jobs from common Adzuna fields."""

        description = str(
            data.get("description") or ""
        ).lower()

        location = data.get("location")

        location_text = ""

        if isinstance(location, dict):
            location_text = " ".join(
                str(value)
                for value in location.values()
                if value is not None
            ).lower()

        searchable_text = (
            f"{description} {location_text}"
        )

        remote_terms = (
            "remote",
            "work from home",
            "work-from-home",
            "wfh",
        )

        return any(
            term in searchable_text
            for term in remote_terms
        )

    @staticmethod
    def _required_string(
        data: dict[str, Any],
        field: str,
    ) -> str:
        value = data.get(field)

        if value is None:
            raise ValueError(
                f"Job field '{field}' is required."
            )

        result = str(value).strip()

        if not result:
            raise ValueError(
                f"Job field '{field}' cannot be empty."
            )

        return result

    @staticmethod
    def _string(
        value: Any,
    ) -> str | None:
        if value is None:
            return None

        result = str(value).strip()

        return result or None

    @staticmethod
    def _to_bool(
        value: Any,
    ) -> bool:
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        if isinstance(value, str):
            return value.strip().lower() in {
                "true",
                "yes",
                "1",
                "remote",
            }

        return bool(value)

    @staticmethod
    def _to_float(
        value: Any,
    ) -> float | None:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            cleaned = re.sub(
                r"[^\d.]",
                "",
                value,
            )

            if not cleaned:
                return None

            try:
                return float(cleaned)
            except ValueError:
                return None

        return None

    def _extract_skills(
        self,
        description: str,
        supplied_skills: Any,
    ) -> list[JobSkill]:
        skills: dict[str, bool] = {}

        if isinstance(supplied_skills, list):
            for value in supplied_skills:
                if isinstance(value, dict):
                    name = value.get("name")
                    required = value.get(
                        "required",
                        True,
                    )

                    if (
                        isinstance(name, str)
                        and name.strip()
                    ):
                        skills[name.strip().lower()] = bool(
                            required
                        )

                elif isinstance(value, str):
                    name = value.strip()

                    if name:
                        skills[name.lower()] = True

        normalized_description = description.lower()

        for skill in self.COMMON_SKILLS:
            if skill.lower() in normalized_description:
                skills.setdefault(
                    skill.lower(),
                    True,
                )

        return [
            JobSkill(
                name=name,
                required=required,
            )
            for name, required in sorted(
                skills.items()
            )
        ]