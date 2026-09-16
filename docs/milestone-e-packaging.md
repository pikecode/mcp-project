# 里程碑 E-3：可复现安装与项目打包

## 目标

让新环境能够根据项目配置安装固定版本的 MCP SDK，并运行同一套测试。

## 项目配置

新增 `pyproject.toml`，声明：

- 项目名称和版本
- Python 最低版本
- MCP SDK 版本
- setuptools 构建方式
- `src/` 下的 Python 模块

核心依赖固定为：

```text
mcp[cli]==2.2.0
```

固定版本可以避免 SDK 自动升级导致示例行为变化。

## 安装方式

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

使用可编辑安装是为了让本地源码修改立即生效，适合当前学习项目。

## 验收结果

```bash
./.venv/bin/python tests/test_server.py
```

结果：

```text
所有测试通过
```

## 当前边界

当前配置支持本地开发和可复现安装，但还没有发布到 PyPI，也没有生成独立 wheel。只有需要对外分发时，才继续完善发布元数据和构建流程。

