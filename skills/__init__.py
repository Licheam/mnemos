"""
Mnemos Skills - AI Agent 记忆系统的核心技能模块

每个 skill 都是一个可被 LLM Agent 调用的函数，包含：
- 清晰的 description（说明何时使用）
- 明确的参数类型和说明
- 返回值说明

可用 Skills:
- summarize_commits: 从 git 历史生成短期记忆
- read_memory: 读取短期/长期记忆
- update_long_term_memory: 更新长期记忆的指定 section
- compress_memory: 压缩过期的短期记忆到长期记忆
"""

from .summarize_commits import summarize_commits
from .read_memory import read_memory, read_short_term, read_long_term
from .write_long_term import update_long_term_memory, VALID_SECTIONS
from .compress_memory import get_memory_stats, extract_old_short_term

__all__ = [
    "summarize_commits",
    "read_memory",
    "read_short_term", 
    "read_long_term",
    "update_long_term_memory",
    "VALID_SECTIONS",
    "get_memory_stats",
    "extract_old_short_term",
]

# Skill 元数据，供 Agent 框架注册使用
SKILL_REGISTRY = {
    "summarize_commits": {
        "function": summarize_commits,
        "description": "从目标项目的 git 提交历史生成短期记忆。读取最近 N 天的 commit 记录，按日期分组写入 short_term.md。应在每次新会话开始时自动调用。",
        "parameters": {},
        "returns": "str - 执行结果消息，包含记录的提交数量",
        "auto_trigger": "session_start",
    },
    "read_memory": {
        "function": read_memory,
        "description": "读取记忆内容。当需要了解项目背景、最近活动、架构决策等信息时调用。",
        "parameters": {
            "memory_type": {
                "type": "str",
                "description": "记忆类型：'short'(短期)、'long'(长期)、'all'(全部)",
                "default": "all",
                "required": False,
            },
            "section": {
                "type": "str", 
                "description": "仅对长期记忆有效。指定读取的 section 名称，如 '项目概述'、'架构决策'",
                "default": None,
                "required": False,
            },
        },
        "returns": "str - 记忆内容的 markdown 文本",
    },
    "update_long_term_memory": {
        "function": update_long_term_memory,
        "description": "更新长期记忆中的指定 section。当对话中出现需要长期记住的项目级信息时调用，如：新的架构决策、代码约定变更、重要的技术选型等。",
        "parameters": {
            "section": {
                "type": "str",
                "description": "要更新的 section 名称，必须是：项目概述/架构决策/代码风格与约定/技术选型/重要约束与注意事项",
                "required": True,
            },
            "content": {
                "type": "str",
                "description": "要写入的内容（markdown 格式）",
                "required": True,
            },
            "mode": {
                "type": "str",
                "description": "'replace' 替换整个 section，'append' 追加到末尾",
                "default": "replace",
                "required": False,
            },
        },
        "returns": "str - 执行结果消息",
    },
    "extract_old_short_term": {
        "function": extract_old_short_term,
        "description": "提取超过指定天数的旧短期记忆，返回待压缩的内容。LLM 应总结这些内容后调用 update_long_term_memory 写入长期记忆。建议每周执行一次或当短期记忆文件过大时执行。",
        "parameters": {
            "days_threshold": {
                "type": "int",
                "description": "超过多少天的记忆视为旧记忆",
                "default": 3,
                "required": False,
            },
        },
        "returns": "str - 提取的旧记忆内容，或提示信息",
    },
    "get_memory_stats": {
        "function": get_memory_stats,
        "description": "获取记忆文件的统计信息（文件大小、行数等）。用于判断是否需要压缩记忆。",
        "parameters": {},
        "returns": "dict - 包含 short_term 和 long_term 的统计信息",
    },
}
