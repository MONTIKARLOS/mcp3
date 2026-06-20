# MCP Web Integration

A Python [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that gives AI assistants tools for HTTP requests, web search, and weather lookups.

## What's inside

| Directory | Description |
|-----------|-------------|
| [`mcp-server/`](mcp-server/) | The MCP server — run this with Claude Desktop or any MCP host |

## Tools

| Tool | What it does |
|------|----------------|
| `fetch_url` | HTTP GET any URL |
| `post_json` | HTTP POST JSON to any URL |
| `search_web` | Search via DuckDuckGo Instant Answer API |
| `get_weather` | Current weather from Open-Meteo (no API key) |
