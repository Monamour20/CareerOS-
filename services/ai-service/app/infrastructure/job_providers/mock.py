from __future__ import annotations

from typing import Any

from app.application.job_ingestion.providers import JobSearchRequest


class MockJobProvider:
    """Deterministic job provider used during development."""

    name = "mock"

    async def search(
        self,
        request: JobSearchRequest,
    ) -> list[dict[str, Any]]:
        jobs = [
            {
                "external_id": "mock-python-backend-001",
                "title": "Python Backend Developer",
                "company": "CareerOS Labs",
                "location": "Mumbai, India",
                "remote": True,
                "employment_type": "full-time",
                "seniority": "entry",
                "description": (
                    "Build backend APIs and AI-powered services "
                    "using Python, FastAPI, PostgreSQL and cloud services."
                ),
                "application_url": "https://example.com/jobs/python-backend",
                "salary_min": 500000,
                "salary_max": 900000,
                "currency": "INR",
                "skills": [
                    {"name": "Python", "required": True},
                    {"name": "FastAPI", "required": True},
                    {"name": "PostgreSQL", "required": True},
                    {"name": "AWS", "required": False},
                ],
            },
            {
                "external_id": "mock-ai-engineer-001",
                "title": "Junior AI Engineer",
                "company": "Nova AI",
                "location": "Bengaluru, India",
                "remote": True,
                "employment_type": "full-time",
                "seniority": "entry",
                "description": (
                    "Develop AI applications using Python, LLMs, "
                    "machine learning pipelines and cloud infrastructure."
                ),
                "application_url": "https://example.com/jobs/ai-engineer",
                "salary_min": 700000,
                "salary_max": 1200000,
                "currency": "INR",
                "skills": [
                    {"name": "Python", "required": True},
                    {"name": "Machine Learning", "required": True},
                    {"name": "LLM", "required": True},
                    {"name": "FastAPI", "required": False},
                    {"name": "AWS", "required": False},
                ],
            },
            {
                "external_id": "mock-cloud-engineer-001",
                "title": "Cloud Engineer",
                "company": "CloudForge",
                "location": "Pune, India",
                "remote": False,
                "employment_type": "full-time",
                "seniority": "junior",
                "description": (
                    "Deploy and maintain cloud applications using "
                    "AWS, Docker, PostgreSQL and Python."
                ),
                "application_url": "https://example.com/jobs/cloud-engineer",
                "salary_min": 600000,
                "salary_max": 1000000,
                "currency": "INR",
                "skills": [
                    {"name": "AWS", "required": True},
                    {"name": "Docker", "required": True},
                    {"name": "Python", "required": True},
                    {"name": "PostgreSQL", "required": False},
                ],
            },
        ]

        filtered = jobs

        if request.query:
            query = request.query.lower()

            filtered = [
                job
                for job in filtered
                if query in job["title"].lower()
                or query in job["description"].lower()
                or any(
                    query in skill["name"].lower()
                    for skill in job["skills"]
                )
            ]

        if request.location:
            location = request.location.lower()

            filtered = [
                job
                for job in filtered
                if job["location"]
                and location in job["location"].lower()
            ]

        if request.remote is not None:
            filtered = [
                job
                for job in filtered
                if job["remote"] == request.remote
            ]

        return filtered[: request.limit]