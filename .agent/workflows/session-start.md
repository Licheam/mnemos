---
description: 新会话启动时的记忆初始化流程
---

# Mnemos 会话启动 Workflow

每次开启新会话时，自动执行以下步骤来初始化 AI Agent 的记忆上下文。

## 步骤

### 1. 更新短期记忆

从目标项目的 git 历史生成最新的短期记忆：

```bash
python /Users/leachim/repo/mnemos/skills/summarize_commits.py
```

这会读取最近 7 天的 git 提交记录，写入 `memory/short_term.md`。

### 2. 读取长期记忆

将长期记忆注入当前会话上下文：

```bash
python -c "from skills.read_memory import read_long_term; print(read_long_term())"
```

请将返回的内容作为项目背景信息理解，在后续对话中参考这些信息：
- **项目概述**：项目的核心目标
- **架构决策**：重要的设计选择
- **代码风格与约定**：编码规范
- **技术选型**：技术栈信息
- **重要约束与注意事项**：需要注意的坑和限制

### 3. 检查记忆状态（可选）

如果需要了解记忆文件的当前状态：

```bash
python -c "from skills.compress_memory import get_memory_stats; import json; print(json.dumps(get_memory_stats(), indent=2))"
```

## 触发条件

- 每次新会话开始时自动执行步骤 1-2
- 如果用户明确要求查看记忆状态，执行步骤 3

## 注意事项

1. 确保 `config.py` 中的 `TARGET_REPO_PATH` 指向正确的目标项目目录
2. 如果目标项目没有 git 仓库，短期记忆将为空
3. 长期记忆需要手动或通过 `update_long_term_memory` skill 填充
