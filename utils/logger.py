import sys
from pathlib import Path
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def init_logger(name: str = "app", log_dir: str | Path = None, level: str = "INFO"):
    """初始化日志器"""
    if log_dir is None:
        log_path = PROJECT_ROOT / "logs"
    else:
        log_path = Path(log_dir)

    log_path.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )

    logger.add(
        log_path / f"{name}.log",
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        encoding="utf-8",
    )

    return logger


logger = init_logger()

__all__ = ["logger", "init_logger"]

if __name__ == '__main__':
    #     use example
    logger.info("hello world")
