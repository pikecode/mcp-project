from pathlib import Path
import anyio

from mcp import Client, StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parents[1]

stdio_server = StdioServerParameters(
    command=str(PROJECT_ROOT / ".venv/bin/python"),
    args=[str(PROJECT_ROOT / "src/server.py")],
)


async def main() -> None:
    async with (
        Client(stdio_server) as local_client,
        Client("http://127.0.0.1:8099/mcp") as http_client,
    ):
        local_tools = await local_client.list_tools()
        http_tools = await http_client.list_tools()

        print("stdio 工具数：", len(local_tools.tools))
        print("HTTP 工具数：", len(http_tools.tools))

        local_result = await local_client.call_tool(
            "add",
            {"a": 1, "b": 2},
        )
        http_result = await http_client.call_tool(
            "add",
            {"a": 10, "b": 20},
        )

        print("stdio 结果：", local_result.structured_content)
        print("HTTP 结果：", http_result.structured_content)


if __name__ == "__main__":
    anyio.run(main)