# 阶段七：编写 MCP Client

## 学习目标

使用 Python MCP Client 主动连接自己的 MCP Server，并调用三类 MCP 能力。

## 内存连接

```python
from mcp import Client
from server import mcp


async with Client(mcp) as client:
    ...
```

`Client(mcp)` 直接连接 Server 对象，不需要端口、子进程或 Inspector，适合测试和学习 Client API。

## 调用 Tool

```python
tools = await client.list_tools()
result = await client.call_tool("add", {"a": 7, "b": 8})
```

工具列表包含名称、描述和输入模式。调用结果中的 `structured_content` 适合程序读取：

```text
{'result': 15}
```

## 读取 Resource

```python
resource = await client.read_resource("notes://intro")
```

Resource 返回 `contents` 列表，需要判断内容类型后再读取 `text` 或其他字段。

## 获取 Prompt

```python
prompt = await client.get_prompt(
    "summarize_note",
    {"text": "MCP 可以让 AI 访问外部工具和数据。"},
)
```

Prompt 返回消息列表。消息包含角色和内容，Client 可以把这些消息交给模型继续处理。

## 验收结果

- Client 成功发现 7 个 Tool
- Client 成功调用 `add` 并得到 `15`
- Client 成功读取 `notes://intro`
- Client 成功获取 `summarize_note`
- 能区分 Tool 的结构化结果、Resource 的内容和 Prompt 的消息

## 下一步

可选扩展是使用 `StdioServerParameters` 让 Client 启动独立的 Server 子进程，之后再学习 Streamable HTTP。

