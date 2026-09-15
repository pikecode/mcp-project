# 阶段十二：管理多个 MCP Server

## 学习目标

让一个 Python 程序同时连接多个 MCP Server，并分别调用它们提供的能力。

## 连接方式

本阶段同时使用：

- stdio Server：由 Client 启动本地子进程
- HTTP Server：连接已经运行的 `http://127.0.0.1:8099/mcp`

每个 Server 都有自己的 Client：

```python
async with (
    Client(stdio_server) as local_client,
    Client("http://127.0.0.1:8099/mcp") as http_client,
):
    ...
```

## 工具调用

两个 Server 都提供 `add`，但调用通过不同 Client 隔离：

```python
local_result = await local_client.call_tool("add", {"a": 1, "b": 2})
http_result = await http_client.call_tool("add", {"a": 10, "b": 20})
```

输出：

```text
stdio 结果： {'result': 3}
HTTP 结果： {'result': 30}
```

## 工具重名

多个 Server 可能暴露同名工具。Host 聚合工具时不能只使用工具名，应该保留来源：

```text
local.add
http.add
```

这样模型或用户才能知道工具实际连接到哪个 Server。

## 验收结果

```text
stdio 工具数： 7
HTTP 工具数： 7
stdio 结果： {'result': 3}
HTTP 结果： {'result': 30}
```

这证明一个 Client 程序可以同时管理不同传输方式的 MCP Server。

## 下一步

可选方向是实现一个简单的工具聚合层，统一列出多个 Server 的能力；涉及工具命名冲突、连接失败和生命周期管理。

