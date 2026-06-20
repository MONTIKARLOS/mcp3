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
