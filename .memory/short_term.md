# 短期记忆

*最后更新: 2026-02-06 17:44*

## 核心变动区域

- `mnemos/cli.py` (7 次修改, +285/-35)
- `.memory/long_term.md` (5 次修改, +103/-2)
- `.memory/short_term.md` (5 次修改, +62/-27)
- `.agent/skills/mnemos/SKILL.md` (5 次修改, +120/-16)
- `templates/.agent/skills/mnemos/SKILL.md` (5 次修改, +125/-16)

## 最近活动

### 2026-02-06

#### 🔧 杂务
- `a257b7f3` chore: Add .gitignore and relocate SKILL.md to a mnemos-specific skill directory.

#### 📝 文档
- `e23b5db0` docs: add GEMINI.md with comprehensive project context and instructions for AI agents.
- `2276946a` docs: update project documentation in README.md

#### ✨ 功能
- `45aebb0f` feat: Implement a configuration system, introduce memory search functionality, and enhance Git commit summarization with updated CLI commands.
- `9f48f082` feat: Implement a configuration system, introduce memory search functionality, and enhance Git commit summarization with updated CLI commands.
- `dc7a8e02` feat: Implement memory search functionality, enhance Git commit summarization with core change area analysis, and add comprehensive unit tests.
- `4d981dec` feat: Enhance `mnemos write` command to accept content from stdin or a file.
- `e4f0a471` feat: Add `--only-skills` option to `mnemos init` to update skills without overwriting existing memory files.
- `a29b8b2c` feat: Add initial markdown files for short-term and long-term memory, and mnemos skill documentation.
- `a55b30c8` feat: add MIT License file
- `95418344` feat: enhance CLI skill management and update skill template.
- `7c3be7ce` feat: Initialize Mnemos agent with memory management, skill system, and a new skill to summarize recent Git commits into short-term memory.

#### 🔨 重构
- `e27aa197` refactor: Restructure project into a `mnemos` package, modularizing skills into `git`, `memory`, and `compress` modules, and introducing a CLI.
