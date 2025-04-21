import logging
import os
import sys
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to console output based on log level"""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m\033[37m",  # White on red background
        "RESET": "\033[0m",  # Reset to default
    }

    def format(self, record):
        format_orig = self._style._fmt

        if record.levelname in self.COLORS:
            self._style._fmt = f"{self.COLORS[record.levelname]}%(asctime)s - %(name)s - %(levelname)s - %(message)s{self.COLORS['RESET']}"
        else:
            self._style._fmt = format_orig

        result = logging.Formatter.format(self, record)
        self._style._fmt = format_orig

        return result


def setup_logger(
    name: Optional[str] = None,
    level: int = logging.INFO,
    log_file: str = "parser.log",
    console_output: bool = True,
) -> logging.Logger:
    """
    Set up and configure a logger with file and optional colored console output.

    Args:
        name: Logger name (uses root logger if None)
        level: Logging level (default: INFO)
        log_file: Path to log file (relative to logs directory)
        console_output: Whether to output logs to console

    Returns:
        Configured logger instance
    """
    logs_dir = Path(__file__).parents[3] / "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_file_path = logs_dir / log_file

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if logger.handlers:
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        colored_formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(colored_formatter)
        logger.addHandler(console_handler)

    return logger


default_logger = setup_logger("car_scraper")
