# MCP Web Integration Server

A production-ready [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes HTTP and web integration tools for AI assistants like Claude.

## Tools

### `fetch_url`
Perform an HTTP GET request to any URL.

**Input:** `url` (string), `headers` (optional object)

**Returns:** JSON with `status`, `body`, and `content_type`

**Example prompt:** _"Fetch https://httpbin.org/get and show me the response."_

---

### `post_json`
Send an HTTP POST request with a JSON body.

**Input:** `url` (string), `payload` (object), `headers` (optional object)

**Returns:** JSON with `status` and `response_body`

**Example prompt:** _"POST `{\"name\": \"test\"}` to https://httpbin.org/post"_

---

### `search_web`
Search the web using the DuckDuckGo Instant Answer API.

**Input:** `query` (string)

**Returns:** Text summary with instant answers and related topics

**Example prompt:** _"Search the web for Python MCP servers."_

---

### `get_weather`
Fetch current weather for a location (free, no API key).

**Input:** `latitude` (number), `longitude` (number)

**Returns:** Temperature (°C), wind speed (km/h), weather code, and description

**Example prompt:** _"What's the weather at latitude 40.71, longitude -74.01?"_

---

## Requirements

- Python 3.11+
- pip

## Setup

### 1. Enter the server directory

```powershell
cd C:\Users\suraj\OneDrive\Desktop\mcp2\mcp-server
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment (optional)

```powershell
copy .env.example .env
```

Edit `.env` if you want to change the timeout or User-Agent.

## Run

```powershell
python main.py
```

The server communicates over **stdio**. It waits for MCP protocol messages on stdin and responds on stdout — do not print to stdout manually. Logs go to stderr.

## Claude Desktop integration

### Config file location

| OS | Path |
|----|------|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

### Windows config (this machine)

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

### Generic config (replace paths)

```json
{
  "mcpServers": {
    "web-integration": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/main.py"]
    }
  }
}
```

Restart Claude Desktop after saving the config. You should see **web-integration** listed under MCP servers with all four tools available.

## Configuration

Settings are loaded from `.env` via `python-dotenv`.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_TIMEOUT` | `15` | HTTP request timeout (seconds) |
| `USER_AGENT` | `MCP-WebIntegration/1.0 ...` | User-Agent header on all requests |
| `OPENWEATHER_API_KEY` | _(empty)_ | Optional; reserved for future use |
| `DUCKDUCKGO_API_KEY` | _(empty)_ | Optional; reserved for future use |

### Example `.env`

```env
DEFAULT_TIMEOUT=15
USER_AGENT=MCP-WebIntegration/1.0 (+https://github.com/modelcontextprotocol)
OPENWEATHER_API_KEY=
DUCKDUCKGO_API_KEY=
```

## Project structure

```
mcp-server/
├── main.py              # Entry point
├── server.py            # MCP server setup (@list_tools, @call_tool)
├── config.py            # Environment configuration
├── tools/
│   ├── __init__.py
│   └── api_tools.py     # Tool definitions and handlers
├── utils/
│   ├── __init__.py
│   └── http_client.py   # Shared async httpx client
├── requirements.txt
├── .env.example
└── README.md
```

## Architecture

```
Claude Desktop
      │
      │  stdio (JSON-RPC)
      ▼
   main.py ──► server.py ──► tools/api_tools.py
                                    │
                                    ▼
                           utils/http_client.py
                                    │
                                    ▼
                              External APIs
                         (httpbin, DuckDuckGo, Open-Meteo)
```

## Error handling

- Every tool is wrapped in try/except — errors never crash the server
- Errors are returned as MCP text content with a clear message
- Errors are logged to **stderr** (stdout is reserved for MCP protocol)
- HTTP connection failures are retried once automatically

## Dependencies

```
mcp[cli]>=1.0.0
httpx>=0.27.0
python-dotenv>=1.0.0
```

## License

MIT
