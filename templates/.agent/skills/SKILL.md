---
name: mnemos
description: AI Agent 记忆系统 - 管理项目的短期记忆和长期记忆
---

# Mnemos - AI Agent 记忆系统

让 AI Agent 具备持久记忆的 skill 包。

## 核心概念

- **短期记忆** (`.memory/short_term.md`): 从 git 提交历史自动生成
- **长期记忆** (`.memory/long_term.md`): 项目级持久信息

## 可用 Skills

### 1. 更新短期记忆

从项目的 git 历史生成短期记忆：

```python
from mnemos import summarize_commits
result = summarize_commits()
print(result)
```

**触发时机**: 每次新会话开始时自动调用。

### 2. 读取记忆

```python
from mnemos import read_memory, read_long_term

# 读取全部记忆
print(read_memory())

# 仅读取长期记忆
print(read_memory("long"))

# 读取特定 section
print(read_long_term("架构决策"))
```

**触发时机**: 需要了解项目背景时调用。

### 3. 更新长期记忆

```python
from mnemos import update_long_term_memory

result = update_long_term_memory(
    section="架构决策",
    content="### 使用 SQLite\n选择 SQLite 作为本地数据库...",
    mode="append"  # 或 "replace"
)
print(result)
```

**可用 section**: 项目概述 / 架构决策 / 代码风格与约定 / 技术选型 / 重要约束与注意事项

**触发时机**: 对话中出现值得长期记住的信息时调用。

### 4. 压缩记忆

```python
from mnemos import extract_old_short_term

old_content = extract_old_short_term(days_threshold=3)
print(old_content)
# 然后总结后调用 update_long_term_memory 写入长期记忆
```

**触发时机**: 每周一次，或短期记忆过大时。

## 会话启动流程

每次开启新会话时：

1. 调用 `summarize_commits()` 更新短期记忆
2. 调用 `read_memory("long")` 读取长期记忆作为上下文
