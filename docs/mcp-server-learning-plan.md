# MCP Server 学习路线

## 0. 总体路线与推进规则

### 总目标

独立设计、开发、测试和部署一个 MCP Server，并理解 Client、传输协议和多 Server Host 的基本架构。

最终作品是一个可运行的本地 Markdown 知识库 MCP 项目，同时具备本地 stdio、HTTP Client、测试、配置和安全边界。

### 五个宏观里程碑

| 里程碑 | 目标 | 状态 |
|---|---|---|
| A. MCP 基础 | 理解协议、Server、Client、Tool、Resource、Prompt | 已完成 |
| B. Server 项目 | 完成本地 Markdown 知识库 Server | 已完成 |
| C. Client 与传输 | 掌握内存、stdio、Streamable HTTP 和错误处理 | 已完成 |
| D. 多 Server Host | 掌握发现、命名空间、注册表和路由 | 已完成 |
| E. 可交付项目 | 完成安全、可靠性、打包、部署和最终验收 | 进行中 |

### 当前主线

当前只推进里程碑 E：

1. 安全边界和远程访问原则：已完成
2. 配置、日志、超时和失败处理：已完成
3. 可复现安装和项目打包：已完成
4. 完整测试和最终 README
5. 最终项目验收与发布提交

### 防偏离规则

- 新内容必须能明确归入当前里程碑，否则暂不学习。
- 不在知识库项目中提前加入数据库、前端、插件市场或复杂框架。
- 每个里程碑只保留一份总结文档；小练习记录在该文档中。
- 每完成一个里程碑再提交一次，不为每个微小练习单独扩展方向。
- 只有当前项目真正需要时，才学习 OAuth、Docker 或其他高级能力。

里程碑 E 的第一部分总结见 `docs/milestone-e-security-boundary.md`。
里程碑 E 的第二部分总结见 `docs/milestone-e-configuration-reliability.md`。
里程碑 E 的第三部分总结见 `docs/milestone-e-packaging.md`。

## 1. 学习目标

使用 Python 从零掌握 Model Context Protocol（模型上下文协议），最终完成一个可实际使用的本地 Markdown 知识库 MCP Server。

最终项目支持：

- 搜索指定目录下的 Markdown 文件
- 读取笔记内容
- 创建新笔记
- 提供一个可复用的知识整理提示词
- 被支持 MCP 的客户端调用

## 2. 学习约定

- 技术栈：Python、MCP Python SDK v2、`MCPServer`
- 连接方式：优先学习 `stdio`
- 数据源：本地 Markdown 文件
- 学习方式：概念 → 最小代码 → 运行验证 → 小练习
- 每个阶段完成验收后再进入下一阶段

第一版不引入数据库、Web 框架、容器、身份认证和多模型适配。这些内容只有在核心流程掌握后才有必要。

## 3. 阶段路线

### 阶段一：理解 MCP 基础

目标：知道 MCP 解决什么问题，以及各组件如何协作。

学习内容：

- MCP Client、MCP Server、Host 的关系
- Tools、Resources、Prompts 的区别
- MCP 与 REST API、函数调用的区别
- `stdio` 传输方式的基本工作流程

练习：

- 画出“客户端调用工具”的流程图
- 用自己的话解释 Tool、Resource、Prompt 各自适合什么场景

验收标准：能够回答“什么时候应该使用 Tool，什么时候应该使用 Resource”。

### 阶段二：创建第一个 MCP Server

目标：让客户端成功调用一个最简单的工具。

学习内容：

- 创建 Python 项目
- 安装 MCP SDK
- 创建 Server
- 注册 `hello` 工具
- 使用 `stdio` 启动服务

练习：实现以下工具：

- `hello(name)`：返回问候语
- `add(a, b)`：返回两个数字的和

验收标准：客户端可以调用两个工具，并能看到正确结果。

### 阶段三：掌握 Tools

目标：理解工具的输入、输出、校验和错误处理。

学习内容：

- 参数类型和必填参数
- 返回字符串、结构化数据和错误信息
- 空输入、非法输入和文件不存在时的处理
- 工具命名和职责边界

练习：实现 `search_files(keyword, directory)`，搜索目录中的 Markdown 文件名。

验收标准：

- 目录不存在时返回明确错误
- 关键词为空时拒绝执行
- 结果为空时返回可理解的提示
- 不通过复制代码实现多个相似工具

### 阶段四：掌握 Resources 和 Prompts

目标：理解“执行动作”和“提供上下文”的区别。

学习内容：

- Resource 如何暴露可读取的数据
- Prompt 如何提供固定任务模板
- Tool、Resource、Prompt 的组合方式

练习：

- 增加一个 Markdown 文件 Resource
- 增加 `summarize_note` Prompt
- 让客户端读取笔记后执行总结任务

验收标准：能够说明为什么“读取笔记”可以设计成 Resource，而“创建笔记”更适合设计成 Tool。

### 阶段五：完成本地知识库 MCP

目标：完成第一个真实项目。

功能范围：

- `search_notes(keyword)`：搜索笔记名称和内容
- `read_note(path)`：读取指定笔记
- `create_note(title, content)`：创建新笔记
- `list_notes()`：列出可访问的笔记
- 一个用于整理笔记的 Prompt

安全要求：

- 只允许访问配置的知识库目录
- 拒绝路径穿越，例如 `../secret.txt`
- 限制可读取的文件类型
- 文件写入失败时保留原有数据

验收标准：能够用客户端完成“搜索一篇笔记 → 读取 → 生成整理结果 → 创建新笔记”的完整流程。

### 阶段六：测试与工程化

目标：让项目可以稳定运行和交接。

学习内容：

- 为路径校验和搜索逻辑添加最小测试
- 统一错误处理
- 使用环境变量或启动参数配置知识库目录
- 编写 README 和运行说明
- 检查日志中不泄露敏感信息

验收标准：

- 核心逻辑有可重复运行的测试
- 新机器可以按照 README 启动项目
- 非法路径和异常文件不会破坏知识库

## 4. 每阶段的固定学习节奏

每个阶段按照以下顺序进行：

1. 先学习当前阶段的一个概念
2. 编写最小可运行版本
3. 实际调用并观察结果
4. 完成一个小练习
5. 运行验收检查
6. 总结本阶段学到的设计原则

遇到错误时，先保留完整错误信息，再定位是客户端、传输层、Server 注册、参数校验还是业务逻辑的问题。

## 5. 阶段总结文档

每完成一个阶段，都在 `docs/` 下新增一份总结文档，作为后续复习笔记。总结文档至少包含：

- 本阶段学到的概念
- 关键代码或命令
- 自己完成的练习
- 遇到的问题和解决方法
- 验收结果
- 仍然不清楚的内容

文件命名格式：

```text
docs/stage-01-mcp-basics.md
docs/stage-02-first-server.md
docs/stage-03-tools.md
```

主路线文档只记录整体计划，不把每次课堂内容全部堆在里面。阶段总结由学习过程逐步生成，避免提前写出没有实际理解的笔记。

## 6. 推荐目录结构

```text
mcp-project/
├── docs/
│   ├── mcp-server-learning-plan.md
│   ├── stage-01-mcp-basics.md
│   └── stage-02-first-server.md
├── src/
│   └── server.py
├── notes/
├── tests/
├── pyproject.toml
└── README.md
```

初期只需要 `server.py` 和少量测试文件。只有代码重复或模块职责明显变复杂时，才拆分更多文件。

## 7. 工程原则

- KISS：先使用最短的可运行实现，避免提前搭建完整框架。
- YAGNI：暂不加入数据库、缓存、权限系统和远程部署。
- SOLID：工具保持单一职责，文件访问逻辑与 MCP 注册逻辑分开。
- DRY：搜索、路径校验等共用逻辑集中实现，避免在每个工具中复制。
- 安全优先：路径访问和文件写入属于信任边界，必须进行校验。

## 8. 完成标准

完成本路线后，应能够：

- 独立解释 MCP 的核心概念
- 独立创建并运行一个 MCP Server
- 判断功能应该设计为 Tool、Resource 还是 Prompt
- 为工具添加参数校验和错误处理
- 防止本地文件访问中的路径穿越
- 编写一个可供他人运行的基础 MCP 项目

## 9. 后续扩展

只有完成上述项目后，再按实际需求选择扩展：

- TypeScript 版本
- HTTP 传输
- 数据库 Resource
- 外部 API Tool
- 用户认证和权限控制
- Docker 部署

扩展顺序以真实需求为准，不为假设中的未来需求提前增加复杂度。

## 10. 阶段七：编写 MCP Client

在完成基础 Server 后，学习使用 Python Client 主动连接 MCP Server：

- 通过 `Client(mcp)` 建立内存连接
- 列出 Server 提供的 Tools
- 调用 Tool 并读取 `structured_content`
- 读取 Resource
- 获取并渲染 Prompt

完成阶段七后，再按需要学习 `stdio` 子进程连接、Streamable HTTP 和多 Server 管理。

## 11. 阶段八：stdio 子进程连接

学习 Client 通过 `StdioServerParameters` 启动独立 MCP Server：

- 使用绝对路径启动项目虚拟环境中的 Python
- 通过 `stdin/stdout` 传输 MCP 消息
- 通过 `env` 传递受控配置
- 理解内存连接与子进程连接的差异

完成阶段八后，可选学习 Streamable HTTP 和多 Server 管理。

## 12. 阶段九：Streamable HTTP

学习 Client 通过 URL 连接 MCP Server：

- 使用 `mcp.run(transport="streamable-http")` 启动 HTTP Server
- 通过 `/mcp` 端点提供 MCP 服务
- 使用 `Client("http://127.0.0.1:<port>/mcp")` 连接
- 理解 HTTP Server 生命周期和端口占用

完成阶段九后，可选学习认证、部署和多 Server 管理。

## 13. 阶段十：Client 错误处理

学习客户端如何处理工具执行失败：

- 使用 `result.is_error` 判断调用是否失败
- 从 `result.content` 读取模型可理解的错误信息
- 区分 ToolError、协议错误和未处理异常
- 不在确认成功前读取或信任 `structured_content`

## 14. 阶段十二：管理多个 MCP Server

学习 Host 同时维护多个 Client 连接：

- 同时连接 stdio 和 Streamable HTTP Server
- 分别发现和调用工具
- 处理不同 Server 中的同名工具
- 为工具增加来源前缀，例如 `local.add`、`http.add`

## 15. 阶段十三：工具聚合与命名空间

学习聚合多个 Server 的工具列表：

- 保留工具来源
- 使用命名空间避免同名冲突
- 先完成名称聚合，再按实际需求实现调用路由

## 16. 阶段十四：工具调用路由

学习根据命名空间把聚合工具路由到正确的 Client：

- 解析 `prefix.tool_name`
- 查找对应 Server Client
- 使用实际工具名发起调用
- 对格式错误和未知 Server 做校验

## 17. 阶段十五：路由器错误处理

学习区分路由层错误和 Server 执行错误：

- 拦截缺少命名空间的工具名
- 拦截未知 Server 前缀
- 保留远程 Tool 的 `is_error` 结果

## 18. 阶段十六：工具注册表

学习在多个 Server 连接建立后构建工具注册表：

- 发现每个 Server 的工具
- 生成 `prefix.tool_name` 映射
- 调用前判断工具是否注册
- 避免每次调用都重新猜测目标工具

## 19. 阶段十七：Server 元数据与能力发现

学习 Client 连接后读取 Server 的运行信息：

- Server 名称和版本
- 协议版本
- Tools、Resources、Prompts 能力
- 根据能力声明动态决定可用操作
