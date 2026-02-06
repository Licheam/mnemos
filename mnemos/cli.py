"""
Mnemos CLI - 命令行工具
"""

import argparse
import shutil
import sys
from pathlib import Path


def get_templates_dir() -> Path:
    """获取模板目录路径"""
    # 开发时：相对于源码目录
    dev_path = Path(__file__).parent.parent / "templates"
    if dev_path.exists():
        return dev_path
    
    # 安装后：在 share 目录
    import sysconfig
    share_path = Path(sysconfig.get_path("data")) / "share" / "mnemos" / "templates"
    if share_path.exists():
        return share_path
    
    raise FileNotFoundError("无法找到模板目录")


def init_project(project_path: str = None, force: bool = False, only_skills: bool = False) -> None:
    """在项目中初始化 .memory 和 .agent/skills 目录"""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    templates_dir = get_templates_dir()
    
    # 复制 .memory 目录
    if not only_skills:
        memory_src = templates_dir / ".memory"
        memory_dst = project_path / ".memory"
        
        if memory_dst.exists() and not force:
            print(f"· 目录已存在: {memory_dst}")
        else:
            if memory_dst.exists():
                shutil.rmtree(memory_dst)
            shutil.copytree(memory_src, memory_dst)
            print(f"✓ 创建/更新目录: {memory_dst}")
    
    # 复制 .agent/skills 目录
    skills_src = templates_dir / ".agent" / "skills"
    skills_dst = project_path / ".agent" / "skills"
    
    if skills_dst.exists() and not force and not only_skills:
        print(f"· 目录已存在: {skills_dst}")
    else:
        skills_dst.parent.mkdir(parents=True, exist_ok=True)
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)
        print(f"✓ 创建/更新目录: {skills_dst}")
    
    print()
    if only_skills:
        print(f"✓ Mnemos Skill 已在 {project_path} 更新完成！")
    else:
        print(f"✓ Mnemos 已在 {project_path} 初始化完成！")
    print()
    print("下一步：")
    if not only_skills:
        print("  1. 编辑 .memory/long_term.md 填写项目基本信息")
    print("  2. 运行 `mnemos update` 生成短期记忆")


def update_memory(project_path: str = None) -> None:
    """更新项目的短期记忆"""
    from . import summarize_commits
    
    if project_path is None:
        project_path = Path.cwd()
    
    result = summarize_commits(str(project_path))
    print(result)


def show_memory(project_path: str = None, memory_type: str = "all") -> None:
    """显示项目的记忆内容"""
    from . import read_memory
    
    if project_path is None:
        project_path = Path.cwd()
    
    content = read_memory(memory_type, project_path=str(project_path))
    print(content)


def write_memory(project_path: str = None, section: str = None, content: str = None, append: bool = False) -> None:
    """更新长期记忆"""
    from . import update_long_term_memory
    
    if project_path is None:
        project_path = Path.cwd()
    
    if not section or not content:
        print("错误：必须指定 --section 和 --content")
        sys.exit(1)
    
    mode = "append" if append else "replace"
    result = update_long_term_memory(section, content, mode, str(project_path))
    print(result)


def compress_memory_cmd(project_path: str = None, days: int = 3) -> None:
    """压缩旧的短期记忆"""
    from . import extract_old_short_term
    
    if project_path is None:
        project_path = Path.cwd()
    
    result = extract_old_short_term(days, str(project_path))
    print(result)


def main():
    """CLI 入口点"""
    parser = argparse.ArgumentParser(
        prog="mnemos",
        description="AI Agent 记忆系统 - 让 AI 具备持久记忆"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="在项目中初始化记忆系统")
    init_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    init_parser.add_argument("-f", "--force", action="store_true", help="强制覆盖已存在的文件")
    init_parser.add_argument("--only-skills", action="store_true", help="只更新 skills 目录，不触碰记忆文件")
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="从 git 历史更新短期记忆")
    update_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示记忆内容")
    show_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    show_parser.add_argument("-t", "--type", choices=["all", "short", "long"], default="all", help="记忆类型")
    
    # write 命令
    write_parser = subparsers.add_parser("write", help="更新长期记忆")
    write_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    write_parser.add_argument("-s", "--section", required=True, help="section 名称")
    write_parser.add_argument("-c", "--content", required=True, help="要写入的内容")
    write_parser.add_argument("-a", "--append", action="store_true", help="追加模式（默认替换）")
    
    # compress 命令
    compress_parser = subparsers.add_parser("compress", help="压缩旧的短期记忆")
    compress_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    compress_parser.add_argument("-d", "--days", type=int, default=3, help="超过多少天视为旧记忆（默认3天）")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_project(args.path, args.force, args.only_skills)
    elif args.command == "update":
        update_memory(args.path)
    elif args.command == "show":
        show_memory(args.path, args.type)
    elif args.command == "write":
        write_memory(args.path, args.section, args.content, args.append)
    elif args.command == "compress":
        compress_memory_cmd(args.path, args.days)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

