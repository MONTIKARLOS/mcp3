"""MCP server setup and tool registration."""

from __future__ import annotations

import logging
from typing import Any

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from tools.api_tools import TOOL_NAMES, execute_tool, get_tool_definitions
from utils.http_client import close_client

logger = logging.getLogger(__name__)

SERVER_NAME = "web-integration"
SERVER_VERSION = "1.0.0"

server = Server(SERVER_NAME)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Expose all web integration tools to MCP clients."""
    return get_tool_definitions()


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict[str, Any] | None,
) -> list[types.TextContent]:
    """Route tool invocations to the appropriate handler."""
    try:
        if name not in TOOL_NAMES:
            message = f"Unknown tool: {name}"
            logger.error(message)
            return [types.TextContent(type="text", text=f"Error: {message}")]

        result = await execute_tool(name, arguments)
        return [types.TextContent(type="text", text=result)]
    except Exception as exc:
        message = f"Unhandled error in tool '{name}': {exc}"
        logger.exception(message)
        return [types.TextContent(type="text", text=f"Error: {message}")]
