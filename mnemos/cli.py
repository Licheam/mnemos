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
    """在项目中初始化 .memory, .agent/skills 和 .mnemos.toml"""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    templates_dir = get_templates_dir()
    
    # 写入配置文件 (.mnemos.toml)
    if not only_skills:
        config_src = templates_dir / ".mnemos.toml"
        config_dst = project_path / ".mnemos.toml"
        if config_dst.exists() and not force:
            print(f"· 配置文件已存在: {config_dst}")
        else:
            shutil.copy2(config_src, config_dst)
            print(f"✓ 创建/更新配置文件: {config_dst}")

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
    from .compress import check_compression_needed
    
    if project_path is None:
        project_path = Path.cwd()
    
    result = summarize_commits(str(project_path))
    print(result)
    
    # 检查是否需要压缩
    needs_comp, reason = check_compression_needed(str(project_path))
    if needs_comp:
        print(f"\n[⚠️ 提醒] {reason}")
        print("建议运行 `mnemos compress` 来归档旧记忆并减小上下文负担。")


def show_memory(project_path: str = None, memory_type: str = "all") -> None:
    """显示项目的记忆内容"""
    from . import read_memory
    
    if project_path is None:
        project_path = Path.cwd()
    
    content = read_memory(memory_type, project_path=str(project_path))
    print(content)


def write_memory(project_path: str = None, section: str = None, content: str = None, file: str = None, append: bool = False) -> None:
    """更新长期记忆"""
    from . import update_long_term_memory
    
    if project_path is None:
        project_path = Path.cwd()
    
    if not section:
        print("错误：必须指定 --section")
        sys.exit(1)

    # 确定内容来源
    final_content = ""
    if file:
        file_path = Path(file)
        if not file_path.exists():
            print(f"错误：文件不存在: {file}")
            sys.exit(1)
        final_content = file_path.read_text(encoding="utf-8")
    elif content:
        if content == "-":
            if sys.stdin.isatty():
                print(f"请输入内容到 [{section}] (按 Ctrl+D 结束):")
            final_content = sys.stdin.read()
        else:
            final_content = content
    else:
        print("错误：必须指定 --content 或 --file")
        sys.exit(1)

    mode = "append" if append else "replace"
    
    # 交互式确认 (仅针对替换操作且在 TTY 环境)
    if mode == "replace" and sys.stdin.isatty():
        confirm = input(f"即将覆盖 [{section}] 的现有内容，确认继续？[y/N]: ")
        if confirm.lower() != 'y':
            print("操作已取消。")
            return

    result = update_long_term_memory(section, final_content, mode, str(project_path))
    print(result)


def compress_memory_cmd(project_path: str = None, days: int = 3) -> None:
    """压缩旧的短期记忆"""
    from . import extract_old_short_term
    
    if project_path is None:
        project_path = Path.cwd()
    
    result = extract_old_short_term(days, str(project_path))
    print(result)


def search_memory_cmd(keyword: str, project_path: str = None, memory_type: str = "all", days: int = None) -> None:
    """在记忆中搜索关键词"""
    from . import search_memory
    
    if project_path is None:
        project_path = Path.cwd()
        
    result = search_memory(keyword, memory_type, days, str(project_path))
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
    write_parser.add_argument("-c", "--content", help="要写入的内容 (使用 '-' 从 stdin 读取)")
    write_parser.add_argument("-f", "--file", help="从指定文件读取内容")
    write_parser.add_argument("-a", "--append", action="store_true", help="追加模式（默认替换）")
    
    # compress 命令
    compress_parser = subparsers.add_parser("compress", help="压缩旧的短期记忆")
    compress_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    compress_parser.add_argument("-d", "--days", type=int, default=3, help="超过多少天视为旧记忆（默认3天）")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="在记忆中搜索关键词")
    search_parser.add_argument("keyword", help="要搜索的关键词")
    search_parser.add_argument("path", nargs="?", default=None, help="项目路径（默认当前目录）")
    search_parser.add_argument("-t", "--type", choices=["all", "short", "long"], default="all", help="搜索范围")
    search_parser.add_argument("-d", "--days", type=int, default=None, help="（仅短期记忆）限定搜索最近几天")

    args = parser.parse_args()
    
    try:
        if args.command == "init":
            init_project(args.path, args.force, args.only_skills)
        elif args.command == "update":
            update_memory(args.path)
        elif args.command == "show":
            show_memory(args.path, args.type)
        elif args.command == "write":
            write_memory(args.path, args.section, args.content, args.file, args.append)
        elif args.command == "compress":
            compress_memory_cmd(args.path, args.days)
        elif args.command == "search":
            search_memory_cmd(args.keyword, args.path, args.type, args.days)
        else:
            parser.print_help()
            sys.exit(1)
    except (FileNotFoundError, ValueError) as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生意外错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

