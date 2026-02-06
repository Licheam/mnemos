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

### 3. 查看记忆

```bash
mnemos show           # 全部记忆
mnemos show -t long   # 仅长期记忆
mnemos show -t short  # 仅短期记忆
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