# 里程碑 F：Codex Host 集成

## 目标

让 Codex 作为 MCP Host，通过本地 stdio 连接当前项目的知识库 MCP Server。

## 配置命令

```bash
codex mcp add mcpKnowledgeBase \
  --env MCP_NOTES_DIR=/Users/peakom/works/mcp-project/notes \
  -- /Users/peakom/works/mcp-project/.venv/bin/python \
  /Users/peakom/works/mcp-project/src/server.py
```

配置查询：

```bash
codex mcp get mcpKnowledgeBase
codex mcp list
```

当前配置：

- 名称：`mcpKnowledgeBase`
- 传输：stdio
- Server：项目虚拟环境中的 Python
- 数据目录：项目下的 `notes/`
- 状态：enabled

## 重要限制

配置修改后，已经运行的 Codex 会话不会自动获得新 MCP 工具。需要新开一个 Codex 会话或重新启动当前客户端。

## 验证任务

新会话中依次验证：

1. 询问可用的知识库工具
2. 搜索 `MCP` 相关笔记
3. 读取 `intro.md`
4. 让模型生成三句话总结
5. 创建一篇测试笔记
6. 再次搜索并读取测试笔记

验证完成后删除测试笔记，避免污染知识库。

## 验收标准

- Codex 能发现 `mcpKnowledgeBase` 的 Tools、Resource 和 Prompt
- Codex 能调用 `search_notes` 和 `read_note`
- 非法路径仍然被 Server 拒绝
- Codex 能读取 ToolError 返回的具体原因
- 测试笔记创建和清理成功

