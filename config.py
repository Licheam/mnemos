import os

# 项目根目录（你的目标项目，不是 mnemos 本身）
TARGET_REPO_PATH = os.environ.get("TARGET_REPO_PATH", ".")

# 记忆文件路径
MEMORY_DIR = os.path.join(os.path.dirname(__file__), "memory")
SHORT_TERM_PATH = os.path.join(MEMORY_DIR, "short_term.md")
LONG_TERM_PATH = os.path.join(MEMORY_DIR, "long_term.md")

# 短期记忆保留的最大 commit 数量
MAX_SHORT_TERM_COMMITS = 20

# 短期记忆保留天数
SHORT_TERM_DAYS = 7