"""
mnemos.doctor - 项目健康诊断工具
"""

import os
import subprocess
from pathlib import Path
from .memory import get_memory_dir, get_long_term_path, get_short_term_path
from .config import get_memory_config_path, load_config


def check_git(project_path: str) -> tuple[bool, str]:
    """检查 Git 环境"""
    try:
        # 检查 git 是否安装
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        # 检查是否在 git 仓库中
        res = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        if res.returncode != 0 or "true" not in res.stdout.lower():
            return False, "当前目录不是 Git 仓库，短期记忆功能将无法使用。"
        return True, "Git 环境正常。"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "未找到 Git 命令，请确保已安装 Git。"


def check_files(project_path: str) -> list[tuple[bool, str]]:
    """检查关键文件是否存在"""
    results = []
    
    # 1. .memory 目录
    memory_dir = get_memory_dir(project_path)
    results.append((memory_dir.exists(), f"记忆目录: {memory_dir}"))
    
    # 2. 长期/短期记忆文件
    results.append((get_long_term_path(project_path).exists(), "长期记忆文件 (long_term.md)"))
    results.append((get_short_term_path(project_path).exists(), "短期记忆文件 (short_term.md)"))
    
    # 3. 配置文件
    results.append((get_memory_config_path(project_path).exists(), "配置文件 (.mnemos.toml)"))
    
    # 4. Skill 文件
    skill_path = Path(project_path) / ".agent" / "skills" / "mnemos" / "SKILL.md"
    results.append((skill_path.exists(), "Agent Skill 定义 (SKILL.md)"))
    
    return results


def run_doctor(project_path: str = None) -> str:
    """运行全项诊断"""
    if project_path is None:
        project_path = os.getcwd()
        
    output = ["=== Mnemos 项目诊断报告 ===", ""]
    is_healthy = True

    # 1. Git 检查
    git_ok, git_msg = check_git(project_path)
    output.append(f"[{'✓' if git_ok else '✗'}] {git_msg}")
    if not git_ok:
        is_healthy = False

    # 2. 文件系统检查
    output.append("\n关键文件状态:")
    for ok, msg in check_files(project_path):
        output.append(f" [{'✓' if ok else '✗'}] {msg}")
        if not ok:
            is_healthy = False

    # 3. 配置检查
    output.append("\n配置合法性:")
    try:
        config = load_config(project_path)
        sections = config.get("memory", {}).get("valid_sections", [])
        if sections:
            output.append(f" [✓] 配置加载成功，定义了 {len(sections)} 个有效 Section。")
        else:
            output.append(" [!] 配置加载成功，但未定义有效 Section。")
    except Exception as e:
        output.append(f" [✗] 配置文件解析失败: {e}")
        is_healthy = False

    output.append("\n" + "="*30)
    if is_healthy:
        output.append("✨ 结论: 项目状态健康。")
    else:
        output.append("⚠️ 结论: 发现潜在问题，请根据上方 [✗] 指示修复。")
        output.append("建议运行 `mnemos init` 重新初始化或修复缺失文件。")

    return "\n".join(output)