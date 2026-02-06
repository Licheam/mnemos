"""
Skill: 压缩短期记忆。
触发时机：定期调用（如每周一次），或短期记忆文件过大时调用。
说明：这个 skill 的核心逻辑需要 LLM 来做摘要，
      这里提供的是"提取待压缩内容"的框架，
      实际的摘要生成应由调用方的 LLM 完成。
"""

import os
import datetime
import sys

# 确保能导入 parent 目录的 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHORT_TERM_PATH, LONG_TERM_PATH


def get_memory_stats() -> dict:
    """获取记忆文件的基本统计信息"""
    stats = {}

    for name, path in [("short_term", SHORT_TERM_PATH), ("long_term", LONG_TERM_PATH)]:
        if os.path.exists(path):
            size = os.path.getsize(path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            line_count = len(content.split("\n"))
            stats[name] = {
                "exists": True,
                "size_bytes": size,
                "line_count": line_count,
            }
        else:
            stats[name] = {"exists": False}

    return stats


def extract_old_short_term(days_threshold: int = 3) -> str:
    """
    提取超过 N 天的短期记忆内容（供 LLM 压缩摘要用）。
    返回这些旧内容的文本，调用方的 LLM 应将其总结后
    通过 write_long_term 写入长期记忆，然后这些旧内容会从短期记忆中删除。
    """
    try:
        with open(SHORT_TERM_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return "短期记忆文件不存在。"

    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days_threshold)).strftime("%Y-%m-%d")

    lines = content.split("\n")
    old_lines = []
    recent_lines = []
    current_date = None
    current_block = []
    is_old = False

    for line in lines:
        if line.startswith("### "):
            # 先保存上一个 block
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

    # 最后一个 block
    if current_block:
        if is_old:
            old_lines.extend(current_block)
        else:
            recent_lines.extend(current_block)

    if not old_lines:
        return "没有需要压缩的旧记忆。"

    # 将 recent 部分写回短期记忆
    header_lines = []
    for line in lines:
        header_lines.append(line)
        if line.startswith("## 最近活动"):
            header_lines.append("")
            break

    new_content = "\n".join(header_lines) + "\n".join(recent_lines)
    with open(SHORT_TERM_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    return (
        "以下是从短期记忆中提取的旧内容，请总结其中的关键信息，"
        "然后调用 update_long_term_memory 写入合适的 section：\n\n"
        + "\n".join(old_lines)
    )

if __name__ == "__main__":
    print(get_memory_stats())
