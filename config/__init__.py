"""
配置加载模块：负责加载和提供配置文件
"""

from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yml"


def load_config() -> dict:
    """
    加载配置文件

    返回:
        dict: 配置字典
    """
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_FILE}")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_config = None


def get_config() -> dict:
    """
    获取配置（单例模式）

    返回:
        dict: 配置字典
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config


def get_model_config() -> dict:
    """获取模型配置"""
    return get_config().get("model", {})


def get_rag_config() -> dict:
    """获取RAG配置"""
    return get_config().get("rag", {})


def get_dirs_config() -> dict:
    """获取目录配置"""
    return get_config().get("dirs", {})


def get_agent_config() -> dict:
    """获取Agent配置"""
    return get_config().get("agent", {})


def get_log_config() -> dict:
    """获取日志配置"""
    return get_config().get("log", {})


__all__ = [
    "load_config",
    "get_config",
    "get_model_config",
    "get_rag_config",
    "get_dirs_config",
    "get_agent_config",
    "get_log_config",
    "CONFIG_FILE",
]