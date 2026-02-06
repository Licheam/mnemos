"""
Skill: 更新长期记忆中的某个 section。
触发时机：对话中出现需要长期记住的项目级信息时调用。
"""

import datetime
import sys
import os

# 确保能导入 parent 目录的 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LONG_TERM_PATH


VALID_SECTIONS = [
    "项目概述",
    "架构决策",
    "代码风格与约定",
    "技术选型",
    "重要约束与注意事项",
]


def update_long_term_memory(section: str, content: str, mode: str = "replace") -> str:
    """
    更新长期记忆中指定 section 的内容。

    Args:
        section: 要更新的 section 名称，必须是以下之一：
                 项目概述 / 架构决策 / 代码风格与约定 / 技术选型 / 重要约束与注意事项
        content: 要写入的内容（markdown 格式）
        mode: "replace" 替换整个 section 内容，"append" 追加到 section 末尾
    """
    if section not in VALID_SECTIONS:
        return f"无效的 section: {section}。可选值: {', '.join(VALID_SECTIONS)}"

    try:
        with open(LONG_TERM_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "长期记忆文件不存在，请先创建模板。"

    # 找到目标 section 的位置
    section_header = f"## {section}"
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if line.strip().startswith(section_header):
            start_idx = i
            continue
        if start_idx is not None and line.strip().startswith("## "):
            end_idx = i
            break

    if start_idx is None:
        return f"在长期记忆中未找到 section: {section}"

    if end_idx is None:
        end_idx = len(lines)

    # 构建新内容
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_section_lines = [f"{section_header}\n", f"*更新于: {now}*\n", "\n", f"{content}\n", "\n"]

    if mode == "append":
        # 保留原有内容，在末尾追加
        existing = lines[start_idx + 1:end_idx]
        new_section_lines = [f"{section_header}\n"] + existing + [f"\n{content}\n", f"*追加于: {now}*\n", "\n"]

    # 替换对应区域
    lines[start_idx:end_idx] = new_section_lines

    with open(LONG_TERM_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return f"长期记忆 [{section}] 已{'追加' if mode == 'append' else '更新'}。"

if __name__ == "__main__":
    # 示例用法
    # print(update_long_term_memory("项目概述", "这是一个示例项目。"))
    pass
