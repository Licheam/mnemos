"""
mnemos.config - 配置管理
"""

import os
import sys
from pathlib import Path

# 尝试导入 tomllib (Python 3.11+), 否则使用默认值
try:
    import tomllib
except ImportError:
    tomllib = None

# 默认配置
DEFAULT_CONFIG = {
    "memory": {
        "valid_sections": [
            "项目概述",
            "架构决策",
            "代码风格与约定",
            "技术选型",
            "重要约束与注意事项"
        ]
    },
    "git": {
        "days": 7,
        "max_count": 50,
        "ignore_files": ["*.lock", "package-lock.json", ".gitignore"]
    },
    "search": {
        "context_lines": 1
    },
    "compression": {
        "max_lines": 500,
        "max_kb": 50
    }
}

def get_config_path(project_path: str = None) -> Path:
    """获取配置文件路径"""
    if project_path is None:
        project_path = os.getcwd()
    return Path(project_path) / ".mnemos.toml"

def load_config(project_path: str = None) -> dict:
    """从项目根目录加载配置，如果不存在则返回默认配置"""
    path = get_memory_config_path(project_path)
    
    config = DEFAULT_CONFIG.copy()
    
    if path.exists() and tomllib:
        try:
            with path.open("rb") as f:
                user_config = tomllib.load(f)
                # 简单的深度合并
                for section, values in user_config.items():
                    if section in config:
                        config[section].update(values)
                    else:
                        config[section] = values
        except Exception as e:
            print(f"警告: 无法加载配置文件 {path}: {e}")
            
    return config

def get_memory_config_path(project_path: str = None) -> Path:
    if project_path is None:
        project_path = os.getcwd()
    return Path(project_path) / ".mnemos.toml"
