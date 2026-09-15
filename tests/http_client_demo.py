import anyio

from mcp import Client


async def main() -> None:
    async with Client("http://127.0.0.1:8099/mcp") as client:
        tools = await client.list_tools()
        print("工具数量：", len(tools.tools))

        result = await client.call_tool("add", {"a": 100, "b": 23})
        print("调用结果：", result.structured_content)


if __name__ == "__main__":
    anyio.run(main)