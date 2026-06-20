"""Shared async HTTP client with retries and default headers."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from config import DEFAULT_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)

_client: httpx.AsyncClient | None = None


def _build_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=httpx.Timeout(DEFAULT_TIMEOUT),
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
    )


def get_client() -> httpx.AsyncClient:
    """Return the shared AsyncClient, creating it on first use."""
    global _client
    if _client is None:
        _client = _build_client()
    return _client


async def close_client() -> None:
    """Close the shared client if it was created."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def request_with_retry(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
) -> httpx.Response:
    """
    Perform an HTTP request with one retry on connection errors.

    Connection-level failures are retried once; HTTP error status codes are
    returned as-is so callers can inspect them.
    """
    client = get_client()
    merged_headers = dict(headers or {})

    last_error: Exception | None = None
    for attempt in range(2):
        try:
            return await client.request(
                method,
                url,
                headers=merged_headers or None,
                json=json,
            )
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout) as exc:
            last_error = exc
            if attempt == 0:
                logger.warning(
                    "Connection error on %s %s (attempt %d): %s",
                    method,
                    url,
                    attempt + 1,
                    exc,
                )
                continue
            raise

    assert last_error is not None
    raise last_error
