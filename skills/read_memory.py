"""
Skill: 读取记忆内容。
触发时机：agent 需要了解项目背景或最近活动时调用。
"""

import sys
import os

# 确保能导入 parent 目录的 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHORT_TERM_PATH, LONG_TERM_PATH


def read_short_term() -> str:
    """读取短期记忆"""
    try:
        with open(SHORT_TERM_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return content if content.strip() else "短期记忆为空。"
    except FileNotFoundError:
        return "短期记忆文件不存在。"


def read_long_term(section: str = None) -> str:
    """
    读取长期记忆。
    
    Args:
        section: 可选，指定读取某个 section，如 "项目概述"、"架构决策"。
                 如果不指定，返回全部长期记忆。
    """
    try:
        with open(LONG_TERM_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return "长期记忆文件不存在。"

    if not section:
        return content if content.strip() else "长期记忆为空。"

    # 按 ## 标题提取对应 section
    lines = content.split("\n")
    capturing = False
    result = []

    for line in lines:
        if line.startswith("## ") and section in line:
            capturing = True
            result.append(line)
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            result.append(line)

    if result:
        return "\n".join(result).strip()
    else:
        return f"未找到 section: {section}"


def read_memory(memory_type: str = "all", section: str = None) -> str:
    """
    主入口：读取记忆制。

    Args:
        memory_type: "short" | "long" | "all"
        section: 仅对长期记忆有效，指定读取的 section 名称
    """
    if memory_type == "short":
        return read_short_term()
    elif memory_type == "long":
        return read_long_term(section)
    else:
        short = read_short_term()
        long = read_long_term()
        return f"{long}\n\n---\n\n{short}"

if __name__ == "__main__":
    print(read_memory())
