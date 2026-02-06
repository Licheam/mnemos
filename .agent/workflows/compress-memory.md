---
description: 压缩过期的短期记忆到长期记忆
---

# 记忆压缩 Workflow

定期将过期的短期记忆压缩归档到长期记忆，保持短期记忆的精简。

## 触发条件

- 每周执行一次（建议周一）
- 短期记忆文件超过 200 行时
- 用户明确要求整理记忆时

## 步骤

### 1. 检查记忆状态

```bash
python -c "from skills.compress_memory import get_memory_stats; import json; print(json.dumps(get_memory_stats(), indent=2, ensure_ascii=False))"
```

查看 `short_term.line_count`，如果超过 200 行，建议执行压缩。

### 2. 提取旧记忆

```bash
python -c "from skills.compress_memory import extract_old_short_term; print(extract_old_short_term(days_threshold=3))"
```

这会：
- 提取超过 3 天的短期记忆
- 将这些旧内容从 short_term.md 中移除
- 返回待压缩的内容

### 3. 总结并写入长期记忆

**这一步需要 LLM 来完成**。

阅读步骤 2 返回的内容，总结其中的关键信息：
- 完成了哪些重要功能？
- 做出了哪些技术决策？
- 发现了哪些问题或坑？
- 有哪些值得记住的模式或经验？

然后调用 `update_long_term_memory` 将总结写入合适的 section：

```python
from skills.write_long_term import update_long_term_memory

# 示例：将开发进度总结追加到项目概述
update_long_term_memory(
    section="项目概述",
    content="### 2024-02-06 周进展\n- 完成了用户认证模块\n- 集成了 PostgreSQL 数据库\n- 修复了并发访问的 bug",
    mode="append"
)

# 示例：将发现的坑追加到注意事项
update_long_term_memory(
    section="重要约束与注意事项",
    content="### PostgreSQL 连接池\n生产环境的连接池大小不要超过 20，否则会触发数据库限制。",
    mode="append"
)
```

## 注意事项

1. 压缩操作会**永久移除**短期记忆中的旧内容，确保已总结后再执行
2. 总结时保留关键信息，丢弃琐碎的日常提交细节
3. 使用 `append` 模式避免覆盖已有的长期记忆
