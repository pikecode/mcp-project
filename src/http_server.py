import os

from server import mcp


if __name__ == "__main__":
    port = int(os.environ.get("MCP_HTTP_PORT", "8099"))

    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=port,
    )