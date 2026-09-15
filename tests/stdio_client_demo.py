from pathlib import Path
import anyio

from mcp import Client, StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parents[1]

server = StdioServerParameters(
    command=str(PROJECT_ROOT / ".venv/bin/python"),
    args=[str(PROJECT_ROOT / "src/server.py")],
    env={
        "MCP_NOTES_DIR": str(PROJECT_ROOT / "notes"),
    },
)


async def main() -> None:
    async with Client(server) as client:
        tools = await client.list_tools()
        print("工具数量：", len(tools.tools))

        result = await client.call_tool("add", {"a": 10, "b": 20})
        print("调用结果：", result.structured_content)


if __name__ == "__main__":
    anyio.run(main)