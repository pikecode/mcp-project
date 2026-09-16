# 阶段十六：工具注册表

## 学习目标

在多个 MCP Server 连接建立后，构建统一的工具注册表，并在调用前校验工具是否存在。

## 注册表结构

逻辑结构：

```text
stdio.add -> (stdio_client, add)
http.add  -> (http_client, add)
```

构建注册表：

```python
async def build_tool_registry(clients: dict[str, object]) -> dict[str, tuple[object, str]]:
    registry = {}

    for prefix, client in clients.items():
        result = await client.list_tools()

        for tool in result.tools:
            registry[f"{prefix}.{tool.name}"] = (client, tool.name)

    return registry
```

## 通过注册表调用

```python
async def call_registered_tool(
    registry: dict[str, tuple[object, str]],
    qualified_name: str,
    arguments: dict[str, object],
):
    if qualified_name not in registry:
        raise ValueError(f"工具未注册：{qualified_name}")

    client, tool_name = registry[qualified_name]
    return await client.call_tool(tool_name, arguments)
```

## 验收结果

正常调用：

```text
注册表调用结果： {'result': 13}
```

未知工具：

```text
未知工具： 工具未注册：http.unknown
```

## 当前边界

当前注册表在连接建立后生成一次。实际系统如果支持 Server 动态增删或工具变更，还需要增加刷新机制和连接状态管理。

