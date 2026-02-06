# Mnemos - AI Agent 记忆系统

让 AI Agent 具备持久记忆的 Python 库。

## 安装

```bash
pip install /path/to/mnemos
```

## 快速开始

### 1. 在项目中初始化

```bash
cd /path/to/your-project
mnemos init
```

这会创建：
- `.memory/` - 记忆文件目录
- `.agent/skills/` - Antigravity Skill 文件

### 2. 更新短期记忆

```bash
mnemos update
```
现在会自动分析 Git 历史，识别变动热点，并按 Conventional Commits 类型（feat, fix, refactor 等）对活动进行智能归类。

### 3. 查看记忆

```bash
mnemos show           # 全部记忆
mnemos show -t long   # 仅长期记忆
mnemos show -t short  # 仅短期记忆
```

### 4. 安全地写入长期记忆

推荐使用 stdin 方式或文件方式，避免 Shell 转义风险：
```bash
# 方式 1：使用文件（最推荐）
mnemos write -s "架构决策" -f decision.md

# 方式 2：使用 Heredoc
mnemos write -s "代码风格与约定" -c - <<'EOF'
### 命名规范
使用 snake_case 命名所有函数。
EOF
```

## Python API

```python
from mnemos import (
    summarize_commits,      # 从 git 历史生成短期记忆
    read_memory,            # 读取记忆
    read_long_term,         # 读取长期记忆
    update_long_term_memory,  # 更新长期记忆
    extract_old_short_term,   # 压缩旧记忆
)

# 更新短期记忆
summarize_commits()

# 读取记忆
print(read_memory("long"))

# 更新长期记忆
update_long_term_memory(
    section="架构决策",
    content="使用 SQLite 作为数据库...",
    mode="append"
)
```

## License

MIT