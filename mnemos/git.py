"""
mnemos.git - Git 历史解析和短期记忆生成
"""

import subprocess
import datetime
import os
from pathlib import Path
from .memory import get_short_term_path


def get_recent_commits(project_path: str = None, days: int = 7, max_count: int = 20) -> list[dict]:
    """
    从项目获取最近 N 天的 git 提交。
    
    Args:
        project_path: 项目路径，默认为当前目录
        days: 获取最近多少天的提交
        max_count: 最大提交数量
    
    Returns:
        提交列表，每个元素包含 hash, date, message, files_changed
    """
    if project_path is None:
        project_path = os.getcwd()
    
    since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    result = subprocess.run(
        [
            "git", "log",
            f"--since={since_date}",
            f"--max-count={max_count}",
            "--pretty=format:%H||%ad||%s",
            "--date=short",
            "--stat",
        ],
        cwd=project_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    raw = result.stdout.strip()
    if not raw:
        return []

    commits = []
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


def summarize_commits(project_path: str = None, days: int = 7) -> str:
    """
    从 git 历史生成短期记忆并写入文件。
    
    Args:
        project_path: 项目路径，默认为当前目录
        days: 获取最近多少天的提交
    
    Returns:
        执行结果消息
    """
    if project_path is None:
        project_path = os.getcwd()
    
    commits = get_recent_commits(project_path, days)
    short_term_path = get_short_term_path(project_path)
    
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
                    stats = [f for f in c["files_changed"] if "changed" in f]
                    if stats:
                        lines.append(f"  - {stats[-1]}")
            lines.append("")

    content = "\n".join(lines)
    
    # 确保目录存在
    short_term_path.parent.mkdir(parents=True, exist_ok=True)
    short_term_path.write_text(content, encoding="utf-8")

    return f"短期记忆已更新，共记录 {len(commits)} 条提交。"
