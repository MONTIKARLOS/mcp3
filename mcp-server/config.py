"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
 
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)


def _get_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return float(raw)


def _get_str(name: str, default: str) -> str:
    return os.getenv(name, default)


DEFAULT_TIMEOUT: float = _get_float("DEFAULT_TIMEOUT", 15.0)

USER_AGENT: str = _get_str(
    "USER_AGENT",
    "MCP-WebIntegration/1.0 (+https://github.com/modelcontextprotocol)",
)

# Optional API keys for future integrations
OPENWEATHER_API_KEY: str | None = os.getenv("OPENWEATHER_API_KEY") or None
DUCKDUCKGO_API_KEY: str | None = os.getenv("DUCKDUCKGO_API_KEY") or None
