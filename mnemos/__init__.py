"""
Mnemos - AI Agent 记忆系统

让 AI Agent 具备持久记忆的库。
"""

from .memory import (
    read_memory,
    read_short_term,
    read_long_term,
    update_long_term_memory,
    get_memory_dir,
    get_short_term_path,
    get_long_term_path,
)
from .git import (
    summarize_commits,
    get_recent_commits,
)
from .compress import (
    get_memory_stats,
    extract_old_short_term,
)
from .search import (
    search_memory,
)

__version__ = "0.1.0"

__all__ = [
    # 读写记忆
    "read_memory",
    "read_short_term",
    "read_long_term",
    "update_long_term_memory",
    # Git 历史
    "summarize_commits",
    "get_recent_commits",
    # 压缩
    "get_memory_stats",
    "extract_old_short_term",
    # 搜索
    "search_memory",
    # 路径
    "get_memory_dir",
    "get_short_term_path",
    "get_long_term_path",
]
