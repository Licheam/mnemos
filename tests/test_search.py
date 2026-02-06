import pytest
from mnemos.search import search_memory

@pytest.fixture
def search_project(tmp_path):
    memory_dir = tmp_path / ".memory"
    memory_dir.mkdir()
    
    long_term = memory_dir / "long_term.md"
    long_term.write_text("## 架构决策\n使用 SQLite 数据库。\n## 项目概述\nMnemos 系统。", encoding="utf-8")
    
    short_term = memory_dir / "short_term.md"
    short_term.write_text("### 2026-02-06\n- 修复了数据库连接 bug。\n### 2026-01-01\n- 旧的活动记录。", encoding="utf-8")
    
    return tmp_path

def test_search_all(search_project):
    result = search_memory("数据库", project_path=str(search_project))
    assert "=== 长期记忆匹配 ===" in result
    assert "架构决策" in result
    assert "=== 短期记忆匹配 ===" in result
    assert "2026-02-06" in result

def test_search_long_only(search_project):
    result = search_memory("数据库", memory_type="long", project_path=str(search_project))
    assert "=== 长期记忆匹配 ===" in result
    assert "=== 短期记忆匹配 ===" not in result

def test_search_days_filter(search_project):
    # 搜索最近 1 天的，应该找不到 2026-01-01 的内容
    result = search_memory("活动", memory_type="short", days=1, project_path=str(search_project))
    assert "未在记忆中找到" in result

def test_search_no_match(search_project):
    result = search_memory("不存在的词", project_path=str(search_project))
    assert "未在记忆中找到" in result