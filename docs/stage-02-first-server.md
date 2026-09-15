# 阶段二：第一个 MCP Server

## 学习目标

使用 Python MCP SDK v2 创建一个最小 MCP Server，并通过 MCP Inspector 调用工具。

## 环境

- Python：3.11.8
- SDK：MCP Python SDK v2
- 传输方式：`stdio`
- 调试工具：MCP Inspector

## 最小服务器结构

```python
from mcp.server import MCPServer

mcp = MCPServer("Learning MCP Server")


@mcp.tool()
def hello(name: str) -> str:
    """向用户返回问候语。"""
    return f"你好，{name}！"


@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b


if __name__ == "__main__":
    mcp.run()
```

## 关键知识

- `MCPServer(...)` 创建服务器实例。
- `@mcp.tool()` 将普通 Python 函数注册为 Tool。
- 函数名会成为工具名。
- 函数文档字符串会成为工具描述。
- 类型提示会生成工具参数模式。
- `mcp.run()` 启动服务器。
- `if __name__ == "__main__":` 防止文件被导入时自动启动服务器。

## 调试方式

在项目目录使用虚拟环境中的命令：

```bash
source .venv/bin/activate
./.venv/bin/mcp dev src/server.py
```

Inspector 使用 `STDIO` 连接，连接后可以在 Tools 页面调用工具。

## 遇到的问题

### 调用了 Anaconda 的旧版 `mcp`

如果堆栈出现 `/opt/anaconda3/bin/mcp`，说明使用的不是项目虚拟环境。解决方式是：

```bash
source .venv/bin/activate
rehash
./.venv/bin/mcp dev src/server.py
```

### Inspector 连接状态为 Disconnected

打开 Inspector 后需要点击 `Connect`。本地学习使用 `STDIO`，不需要手动填写 `localhost:3001` 或其他 HTTP/SSE 地址。

## 验收结果

- `hello("小明")` 返回：`你好，小明！`
- `add(3, 5)` 返回：`8`
- 能够在 Inspector 中查看并调用工具
- 能够理解类型提示如何影响工具输入表单

## 下一阶段

阶段三将学习 Tool 的参数校验、空输入、非法输入和错误处理，并实现第一个文件搜索工具。

