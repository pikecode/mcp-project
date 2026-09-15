from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import server
from mcp.server.mcpserver.exceptions import ToolError


def main() -> None:
    assert "mcp.md" in server.search_notes("MCP")
    assert server.read_note("intro.md")

    try:
        server.read_note("../README.md")
    except ToolError as error:
        assert "只能访问 notes 目录内的文件" in str(error)
    else:
        raise AssertionError("路径穿越没有被拦截")

    try:
        server.read_note("missing.md")
    except ToolError as error:
        assert "笔记不存在" in str(error)
    else:
        raise AssertionError("不存在的笔记没有被拦截")

    print("所有测试通过")


if __name__ == "__main__":
    main()