 
from pathlib import Path
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("Learning MCP Server")
NOTES_DIR = Path(__file__).resolve().parents[1] / "notes"
NOTE_PATH = NOTES_DIR / "intro.md"

@mcp.tool()
def greet(name: str = "") -> str:
    if not name:
        return "你好！"

    return f"你好，{name}！"

@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b

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

@mcp.tool()
def list_notes() -> list[str]:
    """列出知识库中的 Markdown 笔记。"""
    return [
        path.name
        for path in sorted(NOTES_DIR.glob("*.md"))
        if path.is_file()
    ]

@mcp.tool()
def read_note(name: str) -> str:
    """读取一篇 Markdown 笔记。"""
    path = get_note_path(name)

    if not path.is_file():
        raise ToolError(f"笔记不存在：{name}")

    return path.read_text(encoding="utf-8")

@mcp.tool()
def create_note(title: str, content: str) -> str:
    """创建一篇 Markdown 笔记。"""
    title = title.strip()
    content = content.strip()

    if not title:
        raise ToolError("标题不能为空")

    if not content:
        raise ToolError("内容不能为空")

    filename = title if title.lower().endswith(".md") else f"{title}.md"
    path = get_note_path(filename)

    if path.exists():
        raise ToolError(f"笔记已存在：{filename}")

    path.write_text(content + "\n", encoding="utf-8")
    return f"已创建笔记：{filename}"


@mcp.tool()
def search_notes(keyword: str) -> list[str]:
    """搜索笔记名称和内容。"""
    keyword = keyword.strip().casefold()

    if not keyword:
        raise ToolError("关键词不能为空")

    results = []

    for path in sorted(NOTES_DIR.glob("*.md")):
        if keyword in path.name.casefold():
            results.append(path.name)
            continue

        content = path.read_text(encoding="utf-8")
        if keyword in content.casefold():
            results.append(path.name)

    return results

@mcp.resource("notes://intro")
def intro_note() -> str:
    """读取入门笔记。"""
    return NOTE_PATH.read_text(encoding="utf-8")

@mcp.prompt()
def summarize_note(text: str) -> str:
    """生成笔记总结任务。"""
    return f"请用三句话总结以下笔记：\n\n{text}"


def get_note_path(name: str) -> Path:
    """返回知识库内的安全 Markdown 路径。"""
    root = NOTES_DIR.resolve()
    path = (NOTES_DIR / name).resolve()

    try:
        path.relative_to(root)
    except ValueError:
        raise ToolError("只能访问 notes 目录内的文件")

    if path.suffix.lower() != ".md":
        raise ToolError("只能读取 Markdown 文件")

    return path

if __name__ == "__main__":
    mcp.run()