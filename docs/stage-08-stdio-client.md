# 阶段八：stdio 子进程连接

## 学习目标

让 MCP Client 启动一个独立的 Server 子进程，并通过标准输入输出进行 MCP 通信。

## 连接参数

```python
from mcp import Client, StdioServerParameters

server = StdioServerParameters(
    command="/path/to/.venv/bin/python",
    args=["/path/to/src/server.py"],
    env={"MCP_NOTES_DIR": "/path/to/notes"},
)
```

然后交给 Client：

```python
async with Client(server) as client:
    result = await client.call_tool("add", {"a": 10, "b": 20})
```

进入 `async with` 时启动子进程，退出时关闭连接并结束子进程。

## 与内存连接的区别

| 连接方式 | 写法 | 适用场景 |
|---|---|---|
| 内存连接 | `Client(mcp)` | 测试、同一进程内调用 |
| stdio 连接 | `Client(StdioServerParameters(...))` | 独立进程、桌面 Host、真实本地集成 |

stdio 连接不需要端口。Client 启动 Server 后，通过子进程的 `stdin` 和 `stdout` 传输协议消息。

## 关键实践

- 使用项目虚拟环境中的绝对 Python 路径
- 使用 Server 文件的绝对路径
- 通过 `env` 显式传递需要的环境变量
- Server 的 stdout 只能用于 MCP 协议，不要写调试日志
- 调试信息应写入 stderr 或使用 SDK 日志能力

## 验收结果

```text
工具数量： 7
调用结果： {'result': 30}
```

这证明 Client 没有直接导入 Server 对象，而是成功启动了独立子进程并完成了 MCP 调用。

## 下一步

可选方向是 Streamable HTTP：让 Server 监听 HTTP 地址，由 Client 通过 URL 连接。它更接近远程部署，但也会引入端口、生命周期和网络错误处理。

