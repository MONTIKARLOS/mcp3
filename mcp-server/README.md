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
