"""
mnemos.compress - 记忆压缩功能
"""

import os
import datetime
from pathlib import Path
from .memory import get_short_term_path, get_long_term_path


def get_memory_stats(project_path: str = None) -> dict:
    """
    获取记忆文件的统计信息。
    
    Args:
        project_path: 项目路径，默认为当前目录
    
    Returns:
        包含 short_term 和 long_term 统计信息的字典
    """
    if project_path is None:
        project_path = os.getcwd()
    
    stats = {"project_path": project_path}
    
    for name, path in [
        ("short_term", get_short_term_path(project_path)),
        ("long_term", get_long_term_path(project_path))
    ]:
        if path.exists():
            content = path.read_text(encoding="utf-8")
            stats[name] = {
                "exists": True,
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "line_count": len(content.split("\n")),
            }
        else:
            stats[name] = {"exists": False, "path": str(path)}

    return stats


def extract_old_short_term(days_threshold: int = 3, project_path: str = None) -> str:
    """
    提取超过 N 天的短期记忆内容，供 LLM 压缩摘要用。
    
    会从短期记忆中移除这些旧内容，返回待压缩的文本。
    LLM 应总结后调用 update_long_term_memory 写入长期记忆。
    
    Args:
        days_threshold: 超过多少天视为旧记忆
        project_path: 项目路径，默认为当前目录
    
    Returns:
        提取的旧记忆内容，或提示信息
    """
    if project_path is None:
        project_path = os.getcwd()
    
    short_term_path = get_short_term_path(project_path)
    
    try:
        content = short_term_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"短期记忆文件不存在: {short_term_path}"

    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days_threshold)).strftime("%Y-%m-%d")

    lines = content.split("\n")
    old_lines = []
    recent_lines = []
    current_block = []
    is_old = False

    for line in lines:
        if line.startswith("### "):
            if current_block:
                if is_old:
                    old_lines.extend(current_block)
                else:
                    recent_lines.extend(current_block)

            current_date = line.replace("### ", "").strip()
            current_block = [line]
            is_old = current_date < cutoff
        else:
            current_block.append(line)

    if current_block:
        if is_old:
            old_lines.extend(current_block)
        else:
            recent_lines.extend(current_block)

    if not old_lines:
        return "没有需要压缩的旧记忆。"

    # 保留 header 部分
    header_lines = []
    for line in lines:
        header_lines.append(line)
        if line.startswith("## 最近活动"):
            header_lines.append("")
            break

    new_content = "\n".join(header_lines) + "\n".join(recent_lines)
    short_term_path.write_text(new_content, encoding="utf-8")

    return (
        "以下是从短期记忆中提取的旧内容，请总结其中的关键信息，"
        "然后调用 update_long_term_memory 写入合适的 section：\n\n"
        + "\n".join(old_lines)
    )
