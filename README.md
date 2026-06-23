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

## Quick start

```powershell  
cd mcp-server
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python main.py
```

The server runs over **stdio** and is meant to be launched by an MCP host (e.g. Claude Desktop), not used interactively in a terminal.

## Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json 
{
  "mcpServers": {
    "web-integration": {
      "command": "C:\\Users\\suraj\\OneDrive\\Desktop\\mcp2\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\suraj\\OneDrive\\Desktop\\mcp2\\mcp-server\\main.py"]
    }
  }
}
```

Restart Claude Desktop after saving.

## Full documentation

See [`mcp-server/README.md`](mcp-server/README.md) for setup, configuration, project structure, and error handling details.

## Stack

- Python 3.11+
- [mcp](https://github.com/modelcontextprotocol/python-sdk) (official MCP SDK)
- httpx (async HTTP)
- python-dotenv (environment config)
