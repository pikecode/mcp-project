# 阶段六：测试与工程化

## 学习目标

让本地知识库 MCP Server 能够被重复验证、配置和交接。

## 测试

新增 `tests/test_server.py`，使用 Python 标准库 `assert` 验证核心行为：

- 搜索笔记
- 读取正常笔记
- 拦截路径穿越
- 拦截不存在的笔记

运行方式：

```bash
./.venv/bin/python tests/test_server.py
```

测试结果：

```text
所有测试通过
```

当前没有引入测试框架。项目规模较小时，标准库自检足够；当测试数量和夹具明显增加时，再考虑 `pytest`。

## 配置

默认知识库目录由源码位置确定：

```python
DEFAULT_NOTES_DIR = Path(__file__).resolve().parents[1] / "notes"
```

可以通过环境变量覆盖：

```bash
MCP_NOTES_DIR=/path/to/notes ./.venv/bin/mcp dev src/server.py
```

这样既保留了开箱即用的默认值，也支持使用外部知识库目录。

## README

README 现在包含：

- 环境要求
- 安装命令
- 配置方式
- 测试命令
- Inspector 启动命令
- 当前功能和目录结构

## 工具链问题

项目必须使用 `.venv/bin/python` 和 `.venv/bin/mcp`，否则可能误用 Anaconda 的全局 MCP SDK，造成版本不一致。

## 阶段验收

- 测试脚本可以独立运行
- 默认目录配置通过测试
- 自定义 `MCP_NOTES_DIR` 通过测试
- README 可以指导新环境安装和启动
- `.venv/`、`__pycache__/` 和 Python 缓存文件不会进入 Git

## 工程原则

- 使用标准库测试，避免当前阶段增加测试框架依赖
- 使用环境变量解决真实配置需求，不提前引入复杂配置系统
- 使用 `.gitignore` 排除本地环境和生成文件
- 保留清晰的启动命令，降低交接成本

## 学习路线完成情况

阶段一至阶段六已完成：从 MCP 基础、Tool、Resource、Prompt，到本地知识库、安全校验、测试和工程化。

