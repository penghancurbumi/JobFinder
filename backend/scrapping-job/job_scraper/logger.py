"""
Logger — Custom logging configuration.
=======================================

Provides structured logging with separate handlers for
info, error, and scraping statistics. All logs are written
to the logs/ directory.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Log directory from .env or default
LOG_DIR: str = os.getenv("LOG_DIR", "logs")


def setup_logging(log_dir: str | None = None) -> None:
    """
    Configure the logging system with multiple handlers.

    Creates separate log files for:
    - scraping.log: All INFO+ messages (general scraping activity)
    - error.log: WARNING+ messages (errors and warnings only)
    - stats.log: Scraping statistics and summaries

    Args:
        log_dir: Directory to store log files. Defaults to LOG_DIR from .env.
    """
    log_path = Path(log_dir or LOG_DIR)
    log_path.mkdir(parents=True, exist_ok=True)

    # Date suffix for log rotation
    date_suffix = datetime.now().strftime("%Y-%m-%d")

    # Root logger
    root_logger = logging.getLogger("job_scraper")
    root_logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers on re-initialization
    root_logger.handlers.clear()

    # Formatter
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    simple_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )

    # ---- Handler 1: Scraping log (INFO+) ----
    scraping_handler = logging.FileHandler(
        log_path / f"scraping_{date_suffix}.log",
        encoding="utf-8",
    )
    scraping_handler.setLevel(logging.INFO)
    scraping_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(scraping_handler)

    # ---- Handler 2: Error log (WARNING+) ----
    error_handler = logging.FileHandler(
        log_path / f"error_{date_suffix}.log",
        encoding="utf-8",
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)

    # ---- Handler 3: Console (INFO+) ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger under the job_scraper namespace.

    Args:
        name: Logger name (typically module name).

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(f"job_scraper.{name}")


def get_stats_logger() -> logging.Logger:
    """
    Get the dedicated statistics logger.

    This logger writes to a separate stats.log file for
    scraping summaries, counts, and performance metrics.

    Returns:
        Stats logger instance.
    """
    stats_logger = logging.getLogger("job_scraper.stats")

    # Only add handler if not already present
    if not stats_logger.handlers:
        log_path = Path(LOG_DIR)
        log_path.mkdir(parents=True, exist_ok=True)

        date_suffix = datetime.now().strftime("%Y-%m-%d")
        stats_handler = logging.FileHandler(
            log_path / f"stats_{date_suffix}.log",
            encoding="utf-8",
        )
        stats_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        stats_logger.addHandler(stats_handler)

    return stats_logger


# Initialize logging on module import
setup_logging()
