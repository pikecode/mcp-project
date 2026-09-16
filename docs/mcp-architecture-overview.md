# MCP 项目架构总览

## 1. 整体链路

```text
用户请求
   |
   v
MCP Host（当前为 Codex）
   | 发现 Tools / Resources / Prompts
   | 调用工具并接收结果或错误
   v
MCP Client
   |
   +-- stdio --------> src/server.py
   |
   +-- Streamable HTTP -> src/http_server.py -> /mcp
                              |
                              v
                     Learning MCP Server
                              |
              +---------------+----------------+
              |               |                |
           Tools          Resources         Prompts
              |               |                |
        操作 notes/       notes://intro     总结模板
```

## 2. Server 提供的三类能力

### Tools

Tools 是可执行动作，例如：

- `list_notes`：列出笔记
- `read_note`：读取笔记
- `create_note`：创建笔记
- `search_notes`：搜索笔记
- `add`、`greet`：基础学习工具

### Resources

Resource 是可读取的数据资源。当前提供：

- `notes://intro`：入门笔记内容

### Prompts

Prompt 是可复用的任务模板。当前提供：

- `summarize_note`：生成三句话总结任务

## 3. 两种 Transport

| Transport | 入口 | 适用场景 |
|---|---|---|
| stdio | `src/server.py` | 本机 Host 启动子进程 |
| Streamable HTTP | `src/http_server.py` | 通过 URL 连接的客户端 |

Transport 只负责消息传输，不改变 Server 提供的 Tools、Resources 和 Prompts。

## 4. 安全边界

```text
外部输入
   |
   v
参数校验
   |
   +-- 空关键词 -> ToolError
   +-- 非 Markdown -> ToolError
   +-- 路径超出 notes/ -> ToolError
   +-- 文件不存在 -> ToolError
   |
   v
访问 notes/ 文件
```

核心原则是：所有笔记路径都必须解析后确认仍位于 `notes/` 内，不能直接信任 Host 传入的文件名。

## 5. 一次调用的生命周期

1. Host 连接 MCP Server。
2. Client 获取 Server 元数据和能力声明。
3. Host 发现可用工具。
4. Host 选择工具并传入结构化参数。
5. Server 校验参数并执行操作。
6. Server 返回结果，或返回可理解的 ToolError。
7. Host 将结果交给模型继续处理。

## 6. 当前项目的学习结论

- MCP Server 类似能力提供者，不等同于普通业务 API Server。
- Tool 描述动作，Resource 描述数据，Prompt 描述任务模板。
- Host 负责发现和编排，Server 负责执行和保护数据边界。
- stdio 适合本地集成，HTTP 适合独立运行和远程连接。
- 多 Server 场景需要使用命名空间和工具注册表解决同名冲突。

## 7. 下一阶段边界

架构复盘完成后，再按需要学习认证和部署。除非真实场景要求，不提前增加数据库、权限系统或复杂 Agent 编排。
