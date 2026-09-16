# MCP 最终复习

## 一、完整调用链路

```text
Codex（MCP Host）
  -> MCP Client
  -> MCP Server
  -> Tool
  -> 本地资源
  -> 返回结果
```

Host 负责理解用户需求和选择能力，Client 负责连接与通信，Server 负责提供能力，Tool 负责执行具体动作。

## 二、三类 MCP 能力

| 能力 | 含义 | 项目示例 |
|---|---|---|
| Tool | 可执行动作 | `read_note`、`create_note` |
| Resource | 可读取的数据资源 | `notes://intro` |
| Prompt | 可复用的任务模板 | `summarize_note` |

## 三、传输方式

- `stdio`：Host 在本机启动 Server 子进程，适合本地集成。
- `Streamable HTTP`：客户端通过 URL 连接 Server，适合独立运行的服务。

两者只是传输方式不同，Server 提供的 MCP 能力可以保持一致。

## 四、安全边界

`read_note` 只能访问 `notes/` 目录内的 Markdown 文件。

访问 `../README.md` 时必须拒绝，因为它会跳出 `notes/`，形成路径穿越风险。路径校验集中在 Server 的 `get_note_path()` 中，避免不同工具重复实现安全逻辑。

读取 `missing.md` 时应返回明确错误，而不是返回空字符串或自动创建文件。

## 五、最终结论

本项目已经完成从 MCP Server 开发到真实 Host 集成的完整学习闭环：

1. 能创建并运行 MCP Server。
2. 能使用 Tools、Resources 和 Prompts。
3. 能使用 stdio 和 Streamable HTTP。
4. 能连接多个 Server，并处理工具命名空间和路由。
5. 能处理工具错误和路径安全问题。
6. 能让 Codex 作为真实 Host 调用本地 MCP Server。
