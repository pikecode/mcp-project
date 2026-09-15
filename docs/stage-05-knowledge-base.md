# 阶段五：本地 Markdown 知识库 MCP

## 学习目标

把 Tool、Resource 和 Prompt 组合成一个可以实际使用的本地知识库 MCP Server。

## 最终功能

| 能力 | 类型 | 作用 |
|---|---|---|
| `list_notes()` | Tool | 列出所有 Markdown 笔记 |
| `read_note(name)` | Tool | 根据文件名读取笔记 |
| `create_note(title, content)` | Tool | 创建新笔记 |
| `search_notes(keyword)` | Tool | 搜索文件名和文件内容 |
| `notes://intro` | Resource | 提供固定入门笔记 |
| `summarize_note(text)` | Prompt | 生成笔记总结任务 |

## 知识库目录

```python
NOTES_DIR = Path(__file__).resolve().parents[1] / "notes"
```

使用 `__file__` 定位项目目录，避免依赖 Inspector 或启动命令的当前工作目录。

## 路径安全

所有用户提供的文件名都经过统一校验：

```python
def get_note_path(name: str) -> Path:
    root = NOTES_DIR.resolve()
    path = (NOTES_DIR / name).resolve()

    try:
        path.relative_to(root)
    except ValueError:
        raise ToolError("只能访问 notes 目录内的文件")

    if path.suffix.lower() != ".md":
        raise ToolError("只能读取 Markdown 文件")

    return path
```

这可以阻止：

- `../README.md`
- `../escape.md`
- 访问知识库目录以外的文件
- 读取非 Markdown 文件

读取时额外检查文件是否存在，创建时额外检查文件是否已经存在。

## 验收结果

- `list_notes` 成功列出所有笔记
- `read_note("intro.md")` 成功返回内容
- 不存在的笔记返回明确错误
- `create_note` 成功创建 `learning.md`
- 重复标题和空标题可以被校验
- `search_notes("MCP")` 成功搜索文件名和内容
- `search_notes("协议")` 成功搜索中文内容
- 创建笔记时的路径穿越被拦截
- Resource 可以读取 `notes://intro`
- Prompt 可以生成笔记总结任务

## 设计原则

- 使用标准库 `pathlib` 处理文件和路径
- 使用一个路径校验函数处理共享安全逻辑
- 使用 `ToolError` 返回模型可理解、可修正的错误
- 保持工具职责单一
- 使用本地文件作为数据源，不提前引入数据库

## 当前项目能力

现在已经完成一个可用的本地 Markdown 知识库 MCP Server，而不是只有演示性质的 `hello` 工具。下一阶段的重点从功能实现转向测试、配置、文档和工程化。

