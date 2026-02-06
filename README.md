# Mnemos - AI Agent 记忆系统

一个轻量级的 AI Agent 记忆管理系统，使用 Markdown 文件存储短期和长期记忆。

## 核心概念

### 📝 短期记忆 (Short-term Memory)
- 自动从 git 提交历史生成
- 记录最近 7 天的开发活动
- 按日期分组，便于快速浏览
- 存储在 `memory/short_term.md`

### 🧠 长期记忆 (Long-term Memory)
- 手动或通过 skill 更新
- 按 section 组织项目级持久信息
- 包含：项目概述、架构决策、代码风格、技术选型、注意事项
- 存储在 `memory/long_term.md`

## 项目结构

```
mnemos/
├── config.py              # 配置文件
├── init.py                # 初始化脚本
├── memory/
│   ├── long_term.md       # 长期记忆
│   └── short_term.md      # 短期记忆
├── skills/
│   ├── __init__.py        # Skill 注册表
│   ├── summarize_commits.py   # 生成短期记忆
│   ├── read_memory.py     # 读取记忆
│   ├── write_long_term.py # 更新长期记忆
│   └── compress_memory.py # 压缩记忆
└── .agent/
    └── workflows/
        ├── session-start.md   # 会话启动流程
        ├── update-memory.md   # 更新记忆流程
        └── compress-memory.md # 压缩记忆流程
```

## 快速开始

### 1. 初始化

```bash
python init.py
```

### 2. 配置目标项目

编辑 `config.py`，设置 `TARGET_REPO_PATH` 指向你要追踪的项目：

```python
TARGET_REPO_PATH = "/path/to/your/project"
```

或通过环境变量：

```bash
export TARGET_REPO_PATH="/path/to/your/project"
```

### 3. 生成短期记忆

```bash
python skills/summarize_commits.py
```

### 4. 查看记忆

```bash
# 查看全部记忆
python -c "from skills import read_memory; print(read_memory())"

# 仅查看长期记忆
python -c "from skills import read_memory; print(read_memory('long'))"

# 查看特定 section
python -c "from skills import read_long_term; print(read_long_term('架构决策'))"
```

## Skills API

### `summarize_commits()`
从目标项目的 git 历史生成短期记忆。

### `read_memory(memory_type="all", section=None)`
读取记忆内容。
- `memory_type`: `"short"` | `"long"` | `"all"`
- `section`: 仅对长期记忆有效，指定读取的 section

### `update_long_term_memory(section, content, mode="replace")`
更新长期记忆的指定 section。
- `section`: 项目概述 / 架构决策 / 代码风格与约定 / 技术选型 / 重要约束与注意事项
- `content`: Markdown 格式的内容
- `mode`: `"replace"` 替换 | `"append"` 追加

### `extract_old_short_term(days_threshold=3)`
提取超过指定天数的旧短期记忆，供 LLM 压缩摘要用。

### `get_memory_stats()`
获取记忆文件的统计信息。

## Agent 集成

### Skill 注册表

`skills/__init__.py` 提供了 `SKILL_REGISTRY`，包含每个 skill 的：
- `function`: 可调用的函数
- `description`: 功能描述（供 LLM 理解）
- `parameters`: 参数说明
- `returns`: 返回值说明

### 自动触发规则

建议在 Agent 的 system prompt 或配置中添加：

```
每次新会话开始时：
1. 自动调用 summarize_commits() 更新短期记忆
2. 调用 read_memory("long") 并将结果作为项目上下文理解

当对话中出现需要长期记住的信息时：
- 主动调用 update_long_term_memory() 持久化这些信息

每周或短期记忆过大时：
- 调用 extract_old_short_term() 并总结后写入长期记忆
```

## License

MIT