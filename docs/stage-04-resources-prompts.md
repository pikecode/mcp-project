# 阶段四：Resources 和 Prompts

## 学习目标

理解 Tool、Resource、Prompt 的职责区别，并在 Inspector 中分别验证 Resource 读取和 Prompt 生成。

## 三类能力的控制者

| 类型 | 谁决定使用 | 作用 |
|---|---|---|
| Tool | 模型 | 执行动作或改变状态 |
| Resource | 应用 | 提供数据和上下文 |
| Prompt | 用户 | 使用可复用任务模板 |

## Resource 示例

```python
NOTE_PATH = Path(__file__).resolve().parents[1] / "notes" / "intro.md"


@mcp.resource("notes://intro")
def intro_note() -> str:
    """读取入门笔记。"""
    return NOTE_PATH.read_text(encoding="utf-8")
```

Resource 的特点：

- 使用 `@mcp.resource(...)` 注册
- 通过 URI 标识数据
- 调用结果包含 `uri`、`mimeType` 和 `text`
- 读取数据本身不改变系统状态

实际返回结果：

```json
{
  "uri": "notes://intro",
  "mimeType": "text/plain",
  "text": "MCP 是模型上下文协议。\n它让 AI 应用能够以统一方式访问外部工具和数据。"
}
```

## Prompt 示例

```python
@mcp.prompt()
def summarize_note(text: str) -> str:
    """生成笔记总结任务。"""
    return f"请用三句话总结以下笔记：\n\n{text}"
```

Prompt 的特点：

- 使用 `@mcp.prompt()` 注册
- 函数参数是用户提供的模板输入
- 返回值会被包装成消息
- 本身不负责总结，只负责生成任务指令

实际返回结构包含：

```text
role: user
content.type: text
content.text: 请用三句话总结以下笔记：...
```

真正的总结由 AI 模型根据这个 Prompt 和笔记内容完成。

## 设计判断

- 搜索笔记：Tool，因为模型需要主动执行搜索动作
- 创建笔记：Tool，因为会改变文件系统状态
- 读取固定笔记：Resource，因为应用向模型提供数据
- 总结笔记模板：Prompt，因为用户选择一个可复用的任务模板

## 验收结果

- 成功读取 `notes://intro`
- 成功获取 `summarize_note`
- 能解释 Resource 和 Tool 的区别
- 能解释 Prompt 返回的是任务消息，而不是最终总结

## 下一阶段

阶段五将把前面学到的内容组合成一个本地 Markdown 知识库 MCP Server，包括搜索、读取、创建和列出笔记。

