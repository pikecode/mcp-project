from pathlib import Path
import anyio

from mcp import Client, StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parents[1]

stdio_server = StdioServerParameters(
    command=str(PROJECT_ROOT / ".venv/bin/python"),
    args=[str(PROJECT_ROOT / "src/server.py")],
)

async def namespaced_tools(client, prefix: str) -> list[str]:
    result = await client.list_tools()
    return [f"{prefix}.{tool.name}" for tool in result.tools]

async def call_namespaced_tool(
    clients: dict[str, object],
    qualified_name: str,
    arguments: dict[str, object],
):
    try:
        prefix, tool_name = qualified_name.split(".", 1)
    except ValueError:
        raise ValueError("工具名称必须是 prefix.tool_name 格式")

    if prefix not in clients:
        raise ValueError(f"未知的 Server：{prefix}")

    return await clients[prefix].call_tool(tool_name, arguments)

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

        local_names = await namespaced_tools(local_client, "stdio")
        http_names = await namespaced_tools(http_client, "http")
        print("stdio 命名工具：", local_names)
        print("HTTP 命名工具：", http_names)

        clients = {
            "stdio": local_client,
            "http": http_client,
        }

        result = await call_namespaced_tool(
            clients,
            "http.add",
            {"a": 40, "b": 2},
        )

        print("路由调用结果：", result.structured_content)

        for invalid_name in ("add", "unknown.add"):
            try:
                await call_namespaced_tool(
                    clients,
                    invalid_name,
                    {},
                )
            except ValueError as error:
                print(f"{invalid_name}：{error}")     

if __name__ == "__main__":
    anyio.run(main)