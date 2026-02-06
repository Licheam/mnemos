---
description: 更新长期记忆中的指定 section
---

# 更新长期记忆 Workflow

当对话中出现需要长期记住的项目级信息时，使用此 workflow 将信息持久化到长期记忆。

## 使用场景

- 用户描述了项目的核心目标或愿景 → 更新 **项目概述**
- 做出了重要的架构选择 → 更新 **架构决策**
- 约定了编码规范或风格 → 更新 **代码风格与约定**
- 选择或更换了技术栈 → 更新 **技术选型**
- 发现了需要注意的坑或限制 → 更新 **重要约束与注意事项**

## 步骤

### 1. 确定要更新的 Section

可用的 section 名称：
- `项目概述`
- `架构决策`
- `代码风格与约定`
- `技术选型`
- `重要约束与注意事项`

### 2. 执行更新

```python
from skills.write_long_term import update_long_term_memory

# 替换整个 section 的内容
result = update_long_term_memory(
    section="架构决策",
    content="### 模块化设计\n使用插件架构以支持扩展...",
    mode="replace"
)

# 或追加到 section 末尾
result = update_long_term_memory(
    section="重要约束与注意事项", 
    content="### 2024-02-06 发现的问题\n某某 API 有并发限制...",
    mode="append"
)
```

### 3. 验证更新

```bash
python -c "from skills.read_memory import read_long_term; print(read_long_term('架构决策'))"
```

## 内容格式建议

- 使用 `###` 三级标题组织条目
- 每个条目说明 **是什么**、**为什么这样决定**、**有什么影响**
- 适当使用列表提高可读性
- 如果是追加模式，建议在内容开头加上日期标记
