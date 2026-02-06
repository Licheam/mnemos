"""
mnemos.git - Git 历史解析和短期记忆生成
"""

import re
import subprocess
import datetime
import os
from pathlib import Path
from collections import Counter
from .memory import get_short_term_path
from .config import load_config


def parse_commit_type(message: str) -> str:
    """解析 Conventional Commits 类型"""
    # 匹配 "feat: ...", "fix(scope): ...", "chore!: ..." 等格式
    match = re.match(r"^(\w+)(?:\(.*\))?!?:", message)
    if match:
        return match.group(1).lower()
    return "other"


def get_recent_commits(project_path: str = None, days: int = None, max_count: int = None) -> list[dict]:
    """
    从项目获取最近 N 天的 git 提交，包含详细的文件变更数据。
    
    Args:
        project_path: 项目路径，默认为当前目录
        days: 获取最近多少天的提交
        max_count: 最大提交数量
    
    Returns:
        提交列表，每个元素包含 hash, date, message, type, files
    """
    if project_path is None:
        project_path = os.getcwd()

    config = load_config(project_path)
    days = days if days is not None else config["git"]["days"]
    max_count = max_count if max_count is not None else config["git"]["max_count"]
    
    since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    # 使用 --numstat 获取精确的增删行数和文件名
    result = subprocess.run(
        [
            "git", "log",
            f"--since={since_date}",
            f"--max-count={max_count}",
            "--pretty=format:%H||%ad||%s",
            "--date=short",
            "--numstat",
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
        line = line.strip()
        if not line:
            continue
            
        if "||" in line:
            parts = line.split("||", 2)
            if len(parts) == 3:
                if current_commit:
                    commits.append(current_commit)
                current_commit = {
                    "hash": parts[0][:8],
                    "date": parts[1],
                    "message": parts[2],
                    "type": parse_commit_type(parts[2]),
                    "files": [], # List of (added, deleted, filename)
                }
        elif current_commit:
            # 解析 numstat 行: "added deleted filename"
            parts = line.split(None, 2)
            if len(parts) == 3:
                try:
                    # 对于二进制文件，git numstat 会输出 "-"
                    added = int(parts[0]) if parts[0] != "-" else 0
                    deleted = int(parts[1]) if parts[1] != "-" else 0
                    filename = parts[2]
                    current_commit["files"].append((added, deleted, filename))
                except ValueError:
                    pass

    if current_commit:
        commits.append(current_commit)

    return commits


def aggregate_activity(commits: list[dict]) -> dict:
    """
    聚合提交信息，生成统计摘要。
    
    Args:
        commits: 提交列表
        
    Returns:
        包含总计、类型分布和变动热点的字典
    """
    file_stats = {}
    type_counts = Counter()
    
    for c in commits:
        type_counts[c["type"]] += 1
        for added, deleted, filename in c["files"]:
            stats = file_stats.get(filename, {"count": 0, "added": 0, "deleted": 0})
            stats["count"] += 1
            stats["added"] += added
            stats["deleted"] += deleted
            file_stats[filename] = stats
            
    # 排序文件，按修改次数降序
    sorted_files = sorted(
        file_stats.items(), 
        key=lambda x: x[1]["count"], 
        reverse=True
    )
    
    return {
        "total_commits": len(commits),
        "type_distribution": dict(type_counts),
        "hotspots": sorted_files[:5]  # 前 5 个热点文件
    }


def summarize_commits(project_path: str = None, days: int = None) -> str:
    """
    从 git 历史生成结构化的短期记忆。
    
    Args:
        project_path: 项目路径，默认为当前目录
        days: 获取最近多少天的提交
    
    Returns:
        执行结果消息
    """
    if project_path is None:
        project_path = os.getcwd()
    
    if not Path(project_path).joinpath(".git").exists():
         raise FileNotFoundError(f"目录不是 Git 仓库: {project_path}")

    config = load_config(project_path)
    days = days if days is not None else config["git"]["days"]

    commits = get_recent_commits(project_path, days)
    short_term_path = get_short_term_path(project_path)
    
    stats = aggregate_activity(commits)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = [
        "# 短期记忆",
        "",
        f"*最后更新: {now}*",
        "",
        "## 核心变动区域",
        "",
    ]

    if not commits:
        lines.append("暂无最近的提交记录。")
    else:
        # 渲染热点文件
        for filename, info in stats["hotspots"]:
            lines.append(f"- `{filename}` ({info['count']} 次修改, +{info['added']}/-{info['deleted']})")
        lines.append("")
        
        lines.append("## 最近活动")
        lines.append("")

        # 按日期分组
        by_date: dict[str, list] = {}
        for c in commits:
            by_date.setdefault(c["date"], []).append(c)

        # 映射类型到显示文本
        type_labels = {
            "feat": "✨ 功能",
            "fix": "🐛 修复",
            "refactor": "🔨 重构",
            "docs": "📝 文档",
            "test": "✅ 测试",
            "chore": "🔧 杂务",
            "other": "📦 其他"
        }

        for date in sorted(by_date.keys(), reverse=True):
            lines.append(f"### {date}")
            lines.append("")
            
            # 日期内按类型分组
            by_type: dict[str, list] = {}
            for c in by_date[date]:
                by_type.setdefault(c["type"], []).append(c)
                
            for t in sorted(by_type.keys()):
                label = type_labels.get(t, f"📦 {t}")
                lines.append(f"#### {label}")
                for c in by_type[t]:
                    lines.append(f"- `{c['hash']}` {c['message']}")
                lines.append("")

    content = "\n".join(lines)
    
    # 确保目录存在
    short_term_path.parent.mkdir(parents=True, exist_ok=True)
    short_term_path.write_text(content, encoding="utf-8")

    return f"短期记忆已更新，分析了 {len(commits)} 条提交，识别出 {len(stats['hotspots'])} 个变动热点。"