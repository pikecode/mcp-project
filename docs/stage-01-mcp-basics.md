# 阶段一：MCP 基础

## 学习目标

理解 MCP 的基本组成，以及客户端调用 MCP Server 的过程。

## 核心概念

MCP（Model Context Protocol，模型上下文协议）是一套让 AI 应用以统一方式连接外部能力的协议。

基本结构：

```text
用户
  ↓
AI 应用（MCP Host / Client）
  ↓
MCP Server
  ├── Tools：执行操作
  ├── Resources：提供数据
  └── Prompts：提供任务模板
```

## 三种能力

| 类型 | 作用 | 示例 |
|---|---|---|
| Tool | 执行动作或改变状态 | 搜索笔记、创建笔记 |
| Resource | 提供可读取的数据 | 读取固定笔记 |
| Prompt | 提供可复用的任务模板 | 总结一篇笔记 |

判断方法：

- Tool 是“做事情”
- Resource 是“给数据”
- Prompt 是“给模板”

## 一次调用流程

```text
用户提出请求
  ↓
AI 判断需要调用的 Tool
  ↓
MCP Client 发送工具名和参数
  ↓
MCP Server 执行业务逻辑
  ↓
Server 返回结果
  ↓
AI 根据结果回答用户
```

## 与普通后端 API 的区别

MCP Server 本质上也是一种服务，但它按照 MCP 协议向 AI 客户端暴露 Tools、Resources 和 Prompts。普通后端 API 通常面向前端或其他程序，常见形式是 HTTP 接口；MCP 更强调让 AI 能发现并调用外部能力。

## 本地知识库的设计

```text
search_notes(keyword)  -> Tool
read_note(path)        -> Resource 或 Tool
create_note(...)       -> Tool
summarize_note         -> Prompt
```

“读取”是否使用 Resource，要看数据是否固定且可通过 URI 定位；如果需要根据路径、关键词或条件动态读取，也可以使用 Tool。

“创建笔记”属于 Tool，因为它是一个会改变系统状态的动作。

## 本阶段验收

- 能解释 MCP Client、MCP Server、Host 的基本关系
- 能区分 Tool、Resource 和 Prompt
- 能描述一次工具调用的流程
- 能解释创建笔记为什么属于 Tool

## 待后续实践

- MCP Server 的实际启动方式
- `stdio` 传输
- Python SDK v2 的 `MCPServer`
- 第一个可调用的 `hello` 工具

