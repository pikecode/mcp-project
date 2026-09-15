# 阶段十三：工具聚合与命名空间

## 学习目标

在多个 MCP Server 提供同名工具时，保留工具来源并避免命名冲突。

## 命名函数

```python
async def namespaced_tools(client, prefix: str) -> list[str]:
    result = await client.list_tools()
    return [f"{prefix}.{tool.name}" for tool in result.tools]
```

## 聚合结果

stdio Server：

```text
stdio.greet
stdio.add
stdio.search_files
stdio.list_notes
stdio.read_note
stdio.create_note
stdio.search_notes
```

HTTP Server：

```text
http.greet
http.add
http.search_files
http.list_notes
http.read_note
http.create_note
http.search_notes
```

## 为什么需要命名空间

两个 Server 都提供 `add`。如果直接合并，工具名会冲突，Host 无法明确调用目标。

使用来源前缀后：

```text
stdio.add
http.add
```

工具名称本身已经包含来源，后续可以根据前缀找到对应 Client。

## 当前边界

本阶段只完成工具名称聚合，没有实现完整调用路由器。这样可以先验证命名规则，再根据真实需求决定是否增加注册表、连接失败处理和动态路由。

## 验收结果

- 两个 Server 各发现 7 个工具
- 工具名称包含来源前缀
- `stdio.add` 和 `http.add` 可以同时存在

