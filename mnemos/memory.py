"""
mnemos.memory - 记忆读写核心函数
"""

import os
import datetime
from pathlib import Path


def get_memory_dir(project_path: str = None) -> Path:
    """获取记忆目录路径"""
    if project_path is None:
        project_path = os.getcwd()
    return Path(project_path) / ".memory"


def get_short_term_path(project_path: str = None) -> Path:
    """获取短期记忆文件路径"""
    return get_memory_dir(project_path) / "short_term.md"


def get_long_term_path(project_path: str = None) -> Path:
    """获取长期记忆文件路径"""
    return get_memory_dir(project_path) / "long_term.md"


def read_short_term(project_path: str = None) -> str:
    """
    读取短期记忆。
    
    Args:
        project_path: 项目路径，默认为当前目录
    
    Returns:
        短期记忆内容
    """
    path = get_short_term_path(project_path)
    if not path.exists():
        raise FileNotFoundError(f"短期记忆文件不存在: {path}\n请先运行 `mnemos init` 初始化。")
    return path.read_text(encoding="utf-8") or "短期记忆为空。"


def read_long_term(section: str = None, project_path: str = None) -> str:
    """
    读取长期记忆。
    
    Args:
        section: 可选，指定读取的 section 名称（如 "项目概述"）
        project_path: 项目路径，默认为当前目录
    
    Returns:
        长期记忆内容
    """
    path = get_long_term_path(project_path)
    if not path.exists():
        raise FileNotFoundError(f"长期记忆文件不存在: {path}\n请先运行 `mnemos init` 初始化。")
    
    content = path.read_text(encoding="utf-8")

    if not section:
        return content or "长期记忆为空。"

    # 提取指定 section
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

    if not result:
        raise ValueError(f"未找到 section: {section}")
        
    return "\n".join(result).strip()


def read_memory(memory_type: str = "all", section: str = None, project_path: str = None) -> str:
    """
    读取记忆。
    
    Args:
        memory_type: "short" | "long" | "all"
        section: 仅对长期记忆有效，指定 section 名称
        project_path: 项目路径，默认为当前目录
    
    Returns:
        记忆内容
    """
    if memory_type == "short":
        return read_short_term(project_path)
    elif memory_type == "long":
        return read_long_term(section, project_path)
    else:
        long = read_long_term(None, project_path)
        short = read_short_term(project_path)
        return f"{long}\n\n---\n\n{short}"


VALID_SECTIONS = [
    "项目概述",
    "架构决策",
    "代码风格与约定",
    "技术选型",
    "重要约束与注意事项",
]


def update_long_term_memory(section: str, content: str, mode: str = "replace", project_path: str = None) -> str:
    """
    更新长期记忆中的指定 section。
    
    Args:
        section: section 名称（项目概述/架构决策/代码风格与约定/技术选型/重要约束与注意事项）
        content: 要写入的内容（markdown 格式）
        mode: "replace" 替换 | "append" 追加
        project_path: 项目路径，默认为当前目录
    
    Returns:
        执行结果消息
    """
    if section not in VALID_SECTIONS:
        raise ValueError(f"无效的 section: {section}。可选值: {', '.join(VALID_SECTIONS)}")

    path = get_long_term_path(project_path)
    if not path.exists():
        raise FileNotFoundError(f"长期记忆文件不存在: {path}\n请先运行 `mnemos init` 初始化。")
    
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

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
        raise ValueError(f"在长期记忆中未找到 section: {section}")

    if end_idx is None:
        end_idx = len(lines)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if mode == "append":
        existing = lines[start_idx + 1:end_idx]
        new_section = [f"{section_header}\n"] + existing + [f"\n{content}\n", f"*追加于: {now}*\n", "\n"]
    else:
        new_section = [f"{section_header}\n", f"*更新于: {now}*\n", "\n", f"{content}\n", "\n"]

    lines[start_idx:end_idx] = new_section
    path.write_text("".join(lines), encoding="utf-8")

    return f"长期记忆 [{section}] 已{'追加' if mode == 'append' else '更新'}。"
