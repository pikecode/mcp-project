# 阶段三：Tools、参数校验与错误处理

## 学习目标

掌握 Tool 的参数输入、业务校验、文件搜索和错误处理。

## 实现的工具

```python
from pathlib import Path
from mcp.server.mcpserver.exceptions import ToolError


@mcp.tool()
def search_files(keyword: str, directory: str) -> list[str]:
    """搜索目录中名称包含关键词的 Markdown 文件。"""
    keyword = keyword.strip()

    if not keyword:
        raise ToolError("关键词不能为空")

    root = Path(directory)

    if not root.is_dir():
        raise ToolError(f"目录不存在：{directory}")

    return [
        str(path.relative_to(root))
        for path in root.rglob("*.md")
        if keyword.lower() in path.name.lower()
    ]
```

## 两层校验

### SDK 参数校验

函数签名中的类型提示会生成输入模式。例如：

```python
def search_files(keyword: str, directory: str) -> list[str]:
```

如果调用时完全缺少 `keyword`，请求会在函数执行前被 SDK 拒绝，函数内部不会运行。

### 业务规则校验

SDK 无法判断一个字符串是否满足业务要求，因此需要在函数内部校验：

- 去掉空白后，关键词不能为空
- 目录必须存在且确实是目录
- 只搜索 Markdown 文件

## ToolError

对于模型可以修正的工具失败，使用：

```python
raise ToolError("具体错误信息")
```

这样客户端可以看到具体原因，例如：

```text
Error executing tool search_files: 关键词不能为空
```

普通 `ValueError` 会被 SDK 视为未处理异常，客户端通常只能看到：

```text
Error executing tool search_files
```

不要把错误直接作为正常字符串返回，否则客户端会认为 Tool 执行成功。

## 验收结果

- 搜索 `mcp`，得到 `mcp.md`
- 空关键词被拒绝，并返回“关键词不能为空”
- 不存在的目录被拒绝，并返回具体路径
- 没有匹配结果时返回空数组 `[]`
- 理解了 SDK 校验与业务校验的区别

## 工程原则

- 使用标准库 `pathlib` 处理路径
- 复用同一个搜索函数，不复制相似逻辑
- 在信任边界校验外部输入
- 只实现当前需要的文件名搜索，不提前加入全文搜索、缓存或数据库

## 下一阶段

阶段四学习 Resources 和 Prompts，理解“读取数据”“执行动作”和“提供任务模板”的区别。

