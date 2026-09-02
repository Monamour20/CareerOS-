from __future__ import annotations

from typing import Any

import httpx


class JobProviderHTTPClient:
    """Small HTTP client shared by external job providers."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 30.0,
    ):
        self.timeout_seconds = timeout_seconds

    async def get_json(
        self,
        *,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(
            timeout=self.timeout_seconds,
        ) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )

            response.raise_for_status()

            return response.json()