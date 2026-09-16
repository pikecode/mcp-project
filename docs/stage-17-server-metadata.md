# 阶段十七：Server 元数据与能力发现

## 学习目标

让 Client 在连接后读取 Server 身份、版本、协议和能力，而不是依赖硬编码假设。

## Server 元数据

```python
mcp = MCPServer(
    "Learning MCP Server",
    version="0.1.0",
    instructions="这是一个本地 Markdown 知识库 MCP Server。",
)
```

元数据包括：

- Server 名称
- Server 版本
- 给 Host 或模型的使用说明

## Client 读取信息

```python
print(client.server_info.name)
print(client.server_info.version)
print(client.protocol_version)
print(client.server_capabilities.model_dump(exclude_none=True))
```

## 验收结果

```text
Server： Learning MCP Server
版本： 0.1.0
协议： 2026-07-28
能力： {'prompts': {'list_changed': True}, 'resources': {'subscribe': True, 'list_changed': True}, 'tools': {'list_changed': True}}
```

当前 Server 声明了三类能力：

- `tools`
- `resources`
- `prompts`

Client 可以根据能力声明决定是否展示对应界面或发送对应请求。

## 设计意义

能力发现让 Client 不需要假设每个 Server 都支持相同功能。Server 增加或移除能力时，Client 可以在连接阶段发现变化。

