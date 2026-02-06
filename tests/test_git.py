import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from mnemos.git import get_recent_commits, summarize_commits, parse_commit_type

def test_parse_commit_type():
    assert parse_commit_type("feat: add something") == "feat"
    assert parse_commit_type("fix(cli): bug") == "fix"
    assert parse_commit_type("chore!: important杂务") == "chore"
    assert parse_commit_type("Merge branch...") == "other"

def test_get_recent_commits_mocked():
    # 模拟 git log --numstat 的输出
    # 格式: hash||date||message \n added deleted filename
    mock_output = (
        "hash1||2026-02-01||feat: first commit\n"
        "10\t5\tfile1.py\n"
        "hash2||2026-02-02||fix: second commit\n"
        "1\t1\tfile2.py\n"
        "0\t0\timage.png\n"
    )
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_output
        )
        
        commits = get_recent_commits(days=7)
        
        assert len(commits) == 2
        assert commits[0]["type"] == "feat"
        assert len(commits[0]["files"]) == 1
        assert commits[0]["files"][0] == (10, 5, "file1.py")
        
        assert commits[1]["type"] == "fix"
        assert len(commits[1]["files"]) == 2

def test_summarize_commits_success(tmp_path):
    # 模拟一个 git 仓库环境
    (tmp_path / ".git").mkdir()
    memory_dir = tmp_path / ".memory"
    memory_dir.mkdir()
    
    mock_commits = [
        {
            "hash": "abc1234",
            "date": "2026-02-05",
            "message": "feat: fix bug",
            "type": "feat",
            "files": [(10, 2, "main.py")]
        }
    ]
    
    with patch("mnemos.git.get_recent_commits", return_value=mock_commits):
        result = summarize_commits(str(tmp_path))
        assert "变动热点" in result
        
        short_term_file = memory_dir / "short_term.md"
        assert short_term_file.exists()
        content = short_term_file.read_text(encoding="utf-8")
        assert "## 核心变动区域" in content
        assert "main.py" in content
        assert "✨ 功能" in content
        assert "abc1234" in content
