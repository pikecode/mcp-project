# 阶段十四：工具调用路由

## 学习目标

让聚合后的命名工具真正调用对应的 MCP Server。

## 路由函数

```python
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
```

## 调用过程

调用：

```text
http.add
```

解析为：

```text
prefix: http
tool_name: add
```

然后从 Client 注册表中找到 HTTP Client，实际调用：

```python
await http_client.call_tool("add", {"a": 40, "b": 2})
```

## 验收结果

```text
路由调用结果： {'result': 42}
```

这证明工具名称聚合和调用路由已经连通。

## 当前边界

当前路由器仍是教学版：

- 使用简单字典保存 Client
- 使用 `prefix.tool_name` 解析工具
- 未实现动态 Server 注册和连接池
- 未实现 Server 断线重连

这些能力只有在实际需要管理大量 Server 时才值得加入。

