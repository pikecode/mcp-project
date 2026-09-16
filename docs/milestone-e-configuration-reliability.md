# 里程碑 E-2：配置与可靠性

## 目标

在不引入复杂配置系统的前提下，让 HTTP Server、Client 和多 Server 路由具备基本的配置和超时边界。

## 配置

HTTP Server：

```bash
MCP_HTTP_PORT=8099 ./.venv/bin/python src/http_server.py
```

HTTP Client：

```bash
MCP_HTTP_URL=http://127.0.0.1:8099/mcp \\
  ./.venv/bin/python tests/multi_client_demo.py
```

Server 的监听地址仍固定为 `127.0.0.1`，避免通过配置误暴露到公网。

## 超时

注册表调用使用 AnyIO 超时边界：

```python
with anyio.fail_after(timeout_seconds):
    return await client.call_tool(tool_name, arguments)
```

默认超时为 10 秒。超时属于 Client 路由层问题，不应伪装成正常 Tool 结果。

## 日志

当前直接使用 Uvicorn 和 MCP SDK 的 stderr 日志，不增加自定义日志框架。这样足够支持本地学习和故障定位，也避免 stdio 协议被普通 stdout 输出污染。

## 验收结果

- Server 测试通过
- stdio 与 HTTP Client 均发现 7 个工具
- 多 Server 命名空间和注册表路由通过
- `http.add` 正常返回 `42`
- 未知工具和错误路由仍被拦截

## 取舍

当前没有加入自动重试、连接池、日志平台或动态配置文件。只有部署规模和故障模式证明需要时，才增加这些机制。

