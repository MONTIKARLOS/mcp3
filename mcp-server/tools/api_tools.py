"""HTTP and web API tool implementations."""

from __future__ import annotations

import json
import logging
from typing import Any

import mcp.types as types

from utils.http_client import request_with_retry

logger = logging.getLogger(__name__)

# WMO weather interpretation codes (subset) used by Open-Meteo
_WMO_WEATHER_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_tool_definitions() -> list[types.Tool]:
    """Return MCP tool metadata for all registered tools."""
    return [
        types.Tool(
            name="fetch_url",
            description=(
                "Perform an HTTP GET request to any URL and return the response "
                "status code, body, and content type."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch.",
                    },
                    "headers": {
                        "type": "object",
                        "description": "Optional HTTP headers to include in the request.",
                        "additionalProperties": {"type": "string"},
                    },
                },
                "required": ["url"],
            },
        ),
        types.Tool(
            name="post_json",
            description="Send an HTTP POST request with a JSON body to a URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to POST to.",
                    },
                    "payload": {
                        "type": "object",
                        "description": "JSON object to send as the request body.",
                        "additionalProperties": True,
                    },
                    "headers": {
                        "type": "object",
                        "description": "Optional HTTP headers to include in the request.",
                        "additionalProperties": {"type": "string"},
                    },
                },
                "required": ["url", "payload"],
            },
        ),
        types.Tool(
            name="search_web",
            description=(
                "Search the web using the DuckDuckGo Instant Answer API and return "
                "a text summary of top results."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_weather",
            description=(
                "Fetch current weather for a location using Open-Meteo "
                "(free, no API key required)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location.",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location.",
                    },
                },
                "required": ["latitude", "longitude"],
            },
        ),
    ]


async def fetch_url(url: str, headers: dict[str, str] | None = None) -> str:
    """GET a URL and return status, body, and content type as JSON."""
    response = await request_with_retry("GET", url, headers=headers)
    content_type = response.headers.get("content-type", "")
    try:
        body = response.text
    except Exception:
        body = "<binary or undecodable response>"

    result = {
        "status": response.status_code,
        "body": body,
        "content_type": content_type,
    }
    return json.dumps(result, indent=2)


async def post_json(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> str:
    """POST JSON to a URL and return status and response body as JSON."""
    merged_headers = {"Content-Type": "application/json", **(headers or {})}
    response = await request_with_retry(
        "POST",
        url,
        headers=merged_headers,
        json=payload,
    )
    try:
        response_body: Any = response.json()
    except json.JSONDecodeError:
        response_body = response.text

    result = {
        "status": response.status_code,
        "response_body": response_body,
    }
    return json.dumps(result, indent=2, default=str)


def _format_related_topics(topics: list[Any], limit: int = 5) -> list[str]:
    """Extract text summaries from DuckDuckGo related topics."""
    lines: list[str] = []
    for topic in topics:
        if len(lines) >= limit:
            break
        if isinstance(topic, dict):
            if "Text" in topic:
                text = str(topic["Text"]).strip()
                url = topic.get("FirstURL", "")
                if text:
                    lines.append(f"- {text}" + (f" ({url})" if url else ""))
            elif "Topics" in topic:
                for sub in topic.get("Topics", []):
                    if len(lines) >= limit:
                        break
                    if isinstance(sub, dict) and sub.get("Text"):
                        text = str(sub["Text"]).strip()
                        url = sub.get("FirstURL", "")
                        lines.append(f"- {text}" + (f" ({url})" if url else ""))
    return lines


async def search_web(query: str) -> str:
    """Query DuckDuckGo Instant Answer API and return a text summary."""
    from urllib.parse import urlencode

    params = {
        "q": query,
        "format": "json",
        "no_html": "1",
        "skip_disambig": "1",
    }
    url = f"https://api.duckduckgo.com/?{urlencode(params)}"

    response = await request_with_retry("GET", url)
    response.raise_for_status()
    data = response.json()

    parts: list[str] = []

    heading = data.get("Heading")
    if heading:
        parts.append(f"Topic: {heading}")

    if data.get("Answer"):
        parts.append(f"Instant answer: {data['Answer']}")

    abstract = data.get("AbstractText", "").strip()
    if abstract:
        source = data.get("AbstractSource", "")
        url_ref = data.get("AbstractURL", "")
        parts.append(f"Summary: {abstract}")
        if source or url_ref:
            parts.append(f"Source: {source} {url_ref}".strip())

    related = _format_related_topics(data.get("RelatedTopics", []))
    if related:
        parts.append("Related results:")
        parts.extend(related)

    if not parts:
        return f"No instant answer or related topics found for query: {query!r}"

    return "\n".join(parts)


async def get_weather(latitude: float, longitude: float) -> str:
    """Fetch current weather from Open-Meteo for the given coordinates."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m,weather_code"
        "&wind_speed_unit=kmh"
    )

    response = await request_with_retry("GET", url)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    weather_code = int(current.get("weather_code", -1))
    description = _WMO_WEATHER_CODES.get(weather_code, f"Code {weather_code}")

    result = {
        "latitude": latitude,
        "longitude": longitude,
        "temperature_c": current.get("temperature_2m"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "weather_code": weather_code,
        "weather_description": description,
        "observation_time": current.get("time"),
    }
    return json.dumps(result, indent=2)


_TOOL_HANDLERS: dict[str, Any] = {
    "fetch_url": fetch_url,
    "post_json": post_json,
    "search_web": search_web,
    "get_weather": get_weather,
}

TOOL_NAMES: frozenset[str] = frozenset(_TOOL_HANDLERS.keys())


async def execute_tool(name: str, arguments: dict[str, Any] | None) -> str:
    """
    Dispatch a tool call by name.

    Raises KeyError for unknown tools. Individual tool errors are caught,
    logged, and returned as human-readable error strings.
    """
    if name not in _TOOL_HANDLERS:
        raise KeyError(f"Unknown tool: {name}")

    args = arguments or {}
    handler = _TOOL_HANDLERS[name]

    try:
        return await handler(**args)
    except TypeError as exc:
        message = f"Invalid arguments for tool '{name}': {exc}"
        logger.exception(message)
        return f"Error: {message}"
    except Exception as exc:
        message = f"Tool '{name}' failed: {exc}"
        logger.exception(message)
        return f"Error: {message}"
