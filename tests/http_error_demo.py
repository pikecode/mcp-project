import anyio

from mcp import Client
from mcp.types import TextContent


async def main() -> None:
    async with Client("http://127.0.0.1:8099/mcp") as client:
        result = await client.call_tool(
            "read_note",
            {"name": "missing.md"},
        )

        print("是否错误：", result.is_error)

        for item in result.content:
            if isinstance(item, TextContent):
                print("错误信息：", item.text)


if __name__ == "__main__":
    anyio.run(main)