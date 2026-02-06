import pytest
import sys
from unittest.mock import patch
from mnemos.cli import main

def test_cli_show_no_init(tmp_path, capsys):
    """验证未初始化时 show 命令报错并退出码为 1"""
    with patch("os.getcwd", return_value=str(tmp_path)):
        with patch.object(sys, "argv", ["mnemos", "show"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 1
            captured = capsys.readouterr()
            assert "错误:" in captured.out
            assert "请先运行 `mnemos init` 初始化" in captured.out

def test_cli_invalid_command(capsys):
    """验证无效子命令"""
    with patch.object(sys, "argv", ["mnemos", "unknown"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        # argparse 默认对无效命令返回 2 (or 1 depending on version)
        assert excinfo.value.code != 0

def test_cli_write_missing_args(capsys):
    """验证 write 缺失必要参数"""
    with patch.object(sys, "argv", ["mnemos", "write", "-s", "项目概述"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code != 0
