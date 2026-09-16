# 里程碑 E-1：安全边界

## 目标

确保本地 Markdown 知识库 MCP Server 不会因为外部参数访问或写入知识库目录之外的文件，也不会默认暴露到局域网或公网。

## 审计发现

`read_note` 和 `create_note` 原本已经通过 `get_note_path` 限制路径范围，但 `search_files` 接受任意 `directory`，可能搜索知识库之外的目录。

## 修复

`search_files` 现在会：

- 展开用户输入路径
- 解析为绝对路径
- 校验路径位于 `MCP_NOTES_DIR` 内
- 只搜索 Markdown 文件

HTTP Server 继续固定绑定：

```text
127.0.0.1
```

不在本地学习阶段改为 `0.0.0.0`，也不引入自定义认证框架。

## 测试覆盖

- 读取 `../README.md` 被拦截
- 创建 `../escape` 被拦截
- 搜索项目根目录被拦截
- 不存在的笔记被拦截
- 正常 Server、stdio Client 和内存 Client 测试通过

## 安全结论

当前项目适合本机学习和本地 MCP Host 集成。若要开放远程访问，下一步必须增加 HTTPS、认证、访问控制和请求来源校验，不能只修改监听地址。

