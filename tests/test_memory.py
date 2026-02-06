import pytest
import os
from pathlib import Path
from mnemos.memory import (
    get_memory_dir,
    read_short_term,
    read_long_term,
    update_long_term_memory,
    VALID_SECTIONS
)

@pytest.fixture
def temp_project(tmp_path):
    """创建一个带有临时记忆目录的项目环境"""
    memory_dir = tmp_path / ".memory"
    memory_dir.mkdir()
    
    long_term = memory_dir / "long_term.md"
    long_term.write_text("# 项目长期记忆\n\n## 项目概述\n初始概述\n\n## 架构决策\n<!-- -->\n", encoding="utf-8")
    
    short_term = memory_dir / "short_term.md"
    short_term.write_text("# 短期记忆\n\n## 最近活动\n- Initial commit\n", encoding="utf-8")
    
    return tmp_path

def test_get_memory_dir(temp_project):
    expected = temp_project / ".memory"
    assert get_memory_dir(str(temp_project)) == expected

def test_read_short_term_success(temp_project):
    content = read_short_term(str(temp_project))
    assert "最近活动" in content
    assert "Initial commit" in content

def test_read_short_term_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_short_term(str(tmp_path))

def test_read_long_term_full(temp_project):
    content = read_long_term(project_path=str(temp_project))
    assert "# 项目长期记忆" in content
    assert "## 项目概述" in content

def test_read_long_term_section(temp_project):
    content = read_long_term(section="项目概述", project_path=str(temp_project))
    assert "## 项目概述" in content
    assert "初始概述" in content
    assert "## 架构决策" not in content

def test_read_long_term_invalid_section(temp_project):
    with pytest.raises(ValueError, match="未找到 section"):
        read_long_term(section="非对称加密", project_path=str(temp_project))

def test_update_long_term_replace(temp_project):
    new_content = "新的架构内容"
    result = update_long_term_memory(
        section="架构决策",
        content=new_content,
        mode="replace",
        project_path=str(temp_project)
    )
    assert "已更新" in result
    
    # 验证内容
    updated = read_long_term(section="架构决策", project_path=str(temp_project))
    assert new_content in updated
    assert "更新于:" in updated

def test_update_long_term_append(temp_project):
    append_content = "追加的内容"
    update_long_term_memory(
        section="项目概述",
        content=append_content,
        mode="append",
        project_path=str(temp_project)
    )
    
    updated = read_long_term(section="项目概述", project_path=str(temp_project))
    assert "初始概述" in updated
    assert append_content in updated
    assert "追加于:" in updated

def test_update_long_term_invalid_section(temp_project):
    with pytest.raises(ValueError, match="无效的 section"):
        update_long_term_memory("秘密武器", "内容", project_path=str(temp_project))

def test_update_long_term_missing_file(tmp_path):
    # 没有 .memory 目录
    with pytest.raises(FileNotFoundError):
        update_long_term_memory("项目概述", "内容", project_path=str(tmp_path))