# MCP Knowledge Base

一个基于 Python MCP SDK v2 的本地 Markdown 知识库 MCP Server。

## 环境

- Python 3.11+
- MCP Python SDK v2

## 配置

默认读取项目下的 `notes/` 目录。

如需使用其他目录：

```bash
MCP_NOTES_DIR=/path/to/notes ./.venv/bin/mcp dev src/server.py
```

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## 运行测试

```bash
./.venv/bin/python tests/test_server.py
```

## 启动 Inspector

```bash
./.venv/bin/mcp dev src/server.py
```

打开命令输出的 Inspector 地址，点击 Connect。

## 当前能力

- 列出 Markdown 笔记
- 读取笔记
- 创建笔记
- 搜索笔记名称和内容
- 读取 Resource
- 生成总结 Prompt
- 阻止路径穿越

## 安全说明

当前 HTTP Server 仅用于本机学习，绑定地址为 `127.0.0.1`，不会接受局域网或公网访问。

不要将监听地址改为 `0.0.0.0`，除非已经配置认证、HTTPS、访问控制和请求来源校验。

知识库目录通过 `MCP_NOTES_DIR` 指定。Server 会阻止读取、搜索或创建知识库目录之外的文件。

## 目录结构

```text
docs/     学习路线和阶段总结
notes/    Markdown 知识库
src/      MCP Server
tests/    测试
```
