# 阶段十五：路由器错误处理

## 学习目标

让工具路由器在调用前识别本地配置错误，并区分 Server 执行失败。

## 路由层错误

没有命名空间：

```text
add
```

结果：

```text
工具名称必须是 prefix.tool_name 格式
```

未知命名空间：

```text
unknown.add
```

结果：

```text
未知的 Server：unknown
```

这些错误发生在路由器本地，不应该发送到远程 Server。

## Server 执行错误

如果命名空间和工具格式都正确，但 Server 内部执行失败，则由 Client 返回：

```python
result.is_error is True
```

路由器应该保留这个结果，让上层决定如何展示或重试，而不是把所有错误都转换成同一种异常。

## 验收结果

```text
add：工具名称必须是 prefix.tool_name 格式
unknown.add：未知的 Server：unknown
```

## 错误边界

```text
用户输入
  ↓
路由格式校验
  ↓
Server 前缀查找
  ↓
MCP Client 调用
  ↓
Tool 执行结果或 is_error
```

每一层只处理自己能够判断的错误，避免重复处理和错误信息丢失。

