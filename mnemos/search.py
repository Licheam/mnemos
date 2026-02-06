"""
mnemos.search - 记忆搜索功能
"""

import re
import datetime
from pathlib import Path
from .memory import get_long_term_path, get_short_term_path


def search_in_file(path: Path, keyword: str, header_prefix: str) -> list[dict]:
    """
    在 Markdown 文件中搜索关键词，并关联到最近的上级标题。
    
    Returns:
        matches: [{'header': str, 'line_no': int, 'content': str}]
    """
    if not path.exists():
        return []

    results = []
    current_header = "Header"
    lines = path.read_text(encoding="utf-8").splitlines()
    
    # 编译不区分大小写的正则
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for i, line in enumerate(lines):
        # 跟踪当前所在的标题 (如 ## Section 或 ### Date)
        if line.startswith(header_prefix):
            current_header = line.strip().lstrip("#").strip()
            continue
            
        if pattern.search(line):
            # 获取前后各一行的上下文
            start = max(0, i - 1)
            end = min(len(lines), i + 2)
            context = lines[start:end]
            
            results.append({
                "header": current_header,
                "line_no": i + 1,
                "content": line.strip(),
                "context": "\n".join(context)
            })
            
    return results


def search_memory(keyword: str, memory_type: str = "all", days: int = None, project_path: str = None) -> str:
    """
    执行跨文件的记忆搜索。
    """
    output = [f"搜索关键词: '{keyword}'", ""]
    found_any = False

    # 1. 搜索长期记忆
    if memory_type in ("all", "long"):
        path = get_long_term_path(project_path)
        matches = search_in_file(path, keyword, "## ")
        if matches:
            found_any = True
            output.append("=== 长期记忆匹配 ===")
            for m in matches:
                output.append(f"[{m['header']}] L{m['line_no']}: {m['content']}")
            output.append("")

    # 2. 搜索短期记忆
    if memory_type in ("all", "short"):
        path = get_short_term_path(project_path)
        matches = search_in_file(path, keyword, "### ")
        
        # 如果指定了天数，根据标题中的日期过滤
        if days is not None:
            cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
            # 这里的匹配逻辑假设标题格式是 "### YYYY-MM-DD"
            matches = [m for m in matches if m['header'] >= cutoff]

        if matches:
            found_any = True
            output.append("=== 短期记忆匹配 ===")
            for m in matches:
                output.append(f"[{m['header']}] L{m['line_no']}: {m['content']}")
            output.append("")

    if not found_any:
        return f"未在记忆中找到与 '{keyword}' 相关的匹配项。"

    return "\n".join(output)