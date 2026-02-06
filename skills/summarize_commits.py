"""
Skill: 总结最近的 Git 提交记录，写入短期记忆。
触发时机：每次开新会话时调用一次。
"""

import subprocess
import datetime
import sys
import os

# 确保能导入 parent 目录的 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TARGET_REPO_PATH, SHORT_TERM_PATH, SHORT_TERM_DAYS


def get_recent_commits(days: int = SHORT_TERM_DAYS, max_count: int = 20) -> list[dict]:
    """从目标仓库获取最近 N 天的 git 提交"""
    since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    result = subprocess.run(
        [
            "git", "log",
            f"--since={since_date}",
            f"--max-count={max_count}",
            "--pretty=format:%H||%ad||%s",
            "--date=short",
            "--stat",  # 包含文件变更统计
        ],
        cwd=TARGET_REPO_PATH,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    commits = []
    raw = result.stdout.strip()
    if not raw:
        return []

    # 解析每条 commit
    current_commit = None
    for line in raw.split("\n"):
        if "||" in line:
            parts = line.split("||", 2)
            if len(parts) == 3:
                if current_commit:
                    commits.append(current_commit)
                current_commit = {
                    "hash": parts[0][:8],
                    "date": parts[1],
                    "message": parts[2],
                    "files_changed": [],
                }
        elif current_commit and line.strip():
            current_commit["files_changed"].append(line.strip())

    if current_commit:
        commits.append(current_commit)

    return commits


def get_commit_diff_summary(commit_hash: str) -> str:
    """获取单个 commit 的 diff 摘要（仅统计信息，不含完整 diff）"""
    result = subprocess.run(
        ["git", "diff", "--stat", f"{commit_hash}~1", commit_hash],
        cwd=TARGET_REPO_PATH,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def write_short_term_memory(commits: list[dict]) -> str:
    """将 commit 摘要写入短期记忆文件"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# 短期记忆",
        "",
        f"*最后更新: {now}*",
        "",
        "## 最近活动",
        "",
    ]

    if not commits:
        lines.append("暂无最近的提交记录。")
    else:
        # 按日期分组
        by_date: dict[str, list] = {}
        for c in commits:
            by_date.setdefault(c["date"], []).append(c)

        for date in sorted(by_date.keys(), reverse=True):
            lines.append(f"### {date}")
            lines.append("")
            for c in by_date[date]:
                lines.append(f"- `{c['hash']}` {c['message']}")
                if c["files_changed"]:
                    # 只保留最后的统计行
                    stats = [f for f in c["files_changed"] if "changed" in f]
                    if stats:
                        lines.append(f"  - {stats[-1]}")
            lines.append("")

    content = "\n".join(lines)

    with open(SHORT_TERM_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    return f"短期记忆已更新，共记录 {len(commits)} 条提交。"


def summarize_commits() -> str:
    """主入口：获取最近提交并更新短期记忆"""
    commits = get_recent_commits()
    return write_short_term_memory(commits)


if __name__ == "__main__":
    print(summarize_commits())
