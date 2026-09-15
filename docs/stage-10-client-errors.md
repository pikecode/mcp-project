# 阶段十：Client 错误处理

## 学习目标

让 Client 能够识别并处理 Tool 执行失败，而不是把所有失败都当成程序崩溃。

## 调用失败的结果

```python
result = await client.call_tool(
    "read_note",
    {"name": "missing.md"},
)

if result.is_error:
    for item in result.content:
        if isinstance(item, TextContent):
            print(item.text)
else:
    print(result.structured_content)
```

## ToolError 的行为

Server 中抛出：

```python
raise ToolError("笔记不存在：missing.md")
```

Client 收到的是一个正常的 `CallToolResult`：

```text
is_error: True
content: Error executing tool read_note: 笔记不存在：missing.md
```

它不会像普通未处理异常那样直接终止 Client。

## 三个结果字段

| 字段 | 用途 |
|---|---|
| `is_error` | 判断 Tool 是否执行失败 |
| `content` | 模型或用户读取的文本、图片等内容 |
| `structured_content` | 程序读取的结构化成功结果 |

只有 `is_error` 为 `False` 时，才应该信任 `structured_content`。

## 验收结果

```text
是否错误： True
错误信息： Error executing tool read_note: 笔记不存在：missing.md
```

这证明 HTTP Client 可以接收并处理 Server 的业务错误。

## 设计原则

- 预期中的业务失败使用 `ToolError`
- Client 统一检查 `is_error`
- 不把错误字符串伪装成正常返回值
- 不依赖异常文本判断所有结果，优先使用结构化字段

