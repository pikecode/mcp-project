
from pathlib import Path
import sys
import anyio
from mcp.types import TextContent, TextResourceContents

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mcp import Client
from server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("工具列表：", [tool.name for tool in tools.tools])

        result = await client.call_tool("add", {"a": 7, "b": 8})
        print("调用结果：", result.structured_content)

        resource = await client.read_resource("notes://intro")
        for item in resource.contents:
            if isinstance(item, TextResourceContents):
                print("Resource：", item.text)

        prompt = await client.get_prompt(
            "summarize_note",
            {"text": "MCP 可以让 AI 访问外部工具和数据。"},
        )
        for message in prompt.messages:
            if isinstance(message.content, TextContent):
                print("Prompt：", message.content.text)

        print("Server：", client.server_info.name)
        print("版本：", client.server_info.version)
        print("协议：", client.protocol_version)
        print(
            "能力：",
            client.server_capabilities.model_dump(exclude_none=True),
        )


if __name__ == "__main__":
    anyio.run(main)