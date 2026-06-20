"""Entry point for the MCP web integration server."""

from __future__ import annotations

import asyncio
import logging
import sys

from server import run_server


def _configure_logging() -> None:
    """Log to stderr so stdout remains available for MCP stdio transport."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )


def main() -> None:
    """Run the MCP server."""
    _configure_logging()
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
