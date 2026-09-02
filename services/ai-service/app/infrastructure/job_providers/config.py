from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobProviderConfig:
    """Configuration required by an external job provider."""

    name: str
    base_url: str
    api_key: str | None = None
    timeout_seconds: float = 30.0
    credentials: dict[str, str] | None = None