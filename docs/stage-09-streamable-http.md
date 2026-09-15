# 阶段九：Streamable HTTP

## 学习目标

让 MCP Server 监听 HTTP 地址，并让 Python Client 通过 URL 连接。

## HTTP Server

```python
from server import mcp


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8099,
    )
```

启动：

```bash
./.venv/bin/python src/http_server.py
```

服务端点：

```text
http://127.0.0.1:8099/mcp
```

HTTP Server 会持续运行，直到按下 `Ctrl-C`。Client 运行期间必须保持 Server 终端打开。

## HTTP Client

```python
from mcp import Client


async with Client("http://127.0.0.1:8099/mcp") as client:
    tools = await client.list_tools()
    result = await client.call_tool("add", {"a": 100, "b": 23})
```

## 与其他连接方式的区别

| 方式 | Client 参数 | Server 生命周期 |
|---|---|---|
| 内存 | `Client(mcp)` | 和 Client 在同一进程 |
| stdio | `Client(StdioServerParameters(...))` | Client 启动和关闭子进程 |
| HTTP | `Client("http://.../mcp")` | Server 独立监听端口 |

## 常见现象

访问：

```text
http://127.0.0.1:8099/
```

得到 `404 Not Found` 是正常的，因为 MCP 服务在 `/mcp`，根路径没有普通网页。

## 验收结果

```text
工具数量： 7
调用结果： {'result': 123}
```

这证明 Client 已通过 Streamable HTTP 连接 Server，并成功执行 Tool。

## 下一步

可选学习认证、部署、多 Server 管理和 HTTP 错误处理。当前不需要为本地学习项目提前加入这些复杂度。

