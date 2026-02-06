import pytest
import os
from unittest.mock import patch, MagicMock
from mnemos.doctor import run_doctor

@pytest.fixture
def healthy_project(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".mnemos.toml").write_text("[memory]\nvalid_sections = ['A']", encoding="utf-8")
    memory_dir = tmp_path / ".memory"
    memory_dir.mkdir()
    (memory_dir / "long_term.md").write_text("## A", encoding="utf-8")
    (memory_dir / "short_term.md").write_text("# Short", encoding="utf-8")
    
    skill_dir = tmp_path / ".agent" / "skills" / "mnemos"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("Skill", encoding="utf-8")
    
    return tmp_path

def test_doctor_healthy(healthy_project):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="true")
        result = run_doctor(str(healthy_project))
        assert "项目状态健康" in result
        assert "[✓] Git 环境正常" in result

def test_doctor_missing_git(healthy_project):
    # 模拟非 git 仓库
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="false")
        result = run_doctor(str(healthy_project))
        assert "当前目录不是 Git 仓库" in result
        assert "结论: 发现潜在问题" in result

def test_doctor_missing_files(tmp_path):
    # 空目录
    result = run_doctor(str(tmp_path))
    assert "结论: 发现潜在问题" in result
    assert "[✗] 记忆目录" in result
    assert "[✗] 长期记忆文件" in result