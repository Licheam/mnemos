#!/usr/bin/env python3
"""
Mnemos 初始化脚本
首次运行时创建 memory 目录和模板文件
"""

import os
import sys

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(PROJECT_ROOT, "memory")
SKILLS_DIR = os.path.join(PROJECT_ROOT, "skills")

# 模板内容
LONG_TERM_TEMPLATE = """# 项目长期记忆

## 项目概述
<!-- 项目的核心目标和愿景 -->

## 架构决策
<!-- 重要的架构选择及其理由 -->

## 代码风格与约定
<!-- 团队/个人的编码偏好和规范 -->

## 技术选型
<!-- 使用的关键技术栈及选择理由 -->

## 重要约束与注意事项
<!-- 不能忘记的坑、限制、特殊要求 -->
"""

SHORT_TERM_TEMPLATE = """# 短期记忆

## 最近活动

<!-- 由 skill 自动生成，请勿手动编辑此区域以下的内容 -->
"""


def init_memory_dir():
    """创建 memory 目录"""
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
        print(f"✓ 创建目录: {MEMORY_DIR}")
    else:
        print(f"· 目录已存在: {MEMORY_DIR}")


def init_long_term_memory():
    """创建长期记忆模板文件"""
    path = os.path.join(MEMORY_DIR, "long_term.md")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(LONG_TERM_TEMPLATE)
        print(f"✓ 创建文件: {path}")
    else:
        print(f"· 文件已存在: {path}")


def init_short_term_memory():
    """创建短期记忆模板文件"""
    path = os.path.join(MEMORY_DIR, "short_term.md")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(SHORT_TERM_TEMPLATE)
        print(f"✓ 创建文件: {path}")
    else:
        print(f"· 文件已存在: {path}")


def init_skills_dir():
    """确保 skills 目录存在"""
    if not os.path.exists(SKILLS_DIR):
        os.makedirs(SKILLS_DIR)
        print(f"✓ 创建目录: {SKILLS_DIR}")
    else:
        print(f"· 目录已存在: {SKILLS_DIR}")


def check_config():
    """检查配置文件"""
    config_path = os.path.join(PROJECT_ROOT, "config.py")
    if os.path.exists(config_path):
        print(f"✓ 配置文件存在: {config_path}")
        
        # 读取并显示当前配置
        from config import TARGET_REPO_PATH, SHORT_TERM_DAYS, MAX_SHORT_TERM_COMMITS
        print(f"  - TARGET_REPO_PATH: {TARGET_REPO_PATH}")
        print(f"  - SHORT_TERM_DAYS: {SHORT_TERM_DAYS}")
        print(f"  - MAX_SHORT_TERM_COMMITS: {MAX_SHORT_TERM_COMMITS}")
    else:
        print(f"✗ 配置文件不存在: {config_path}")
        return False
    return True


def main():
    print("=" * 50)
    print("Mnemos - AI Agent 记忆系统初始化")
    print("=" * 50)
    print()
    
    # 初始化目录和文件
    init_memory_dir()
    init_skills_dir()
    init_long_term_memory()
    init_short_term_memory()
    
    print()
    
    # 检查配置
    if not check_config():
        print("\n请先创建 config.py 配置文件！")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("✓ 初始化完成！")
    print()
    print("下一步:")
    print("1. 编辑 config.py 设置 TARGET_REPO_PATH 指向你的目标项目")
    print("2. 运行 `python skills/summarize_commits.py` 测试短期记忆生成")
    print("3. 编辑 memory/long_term.md 填写项目的长期记忆")
    print("=" * 50)


if __name__ == "__main__":
    main()
