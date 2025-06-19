import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# Import directly from project root
from constants import LOG_DIR, LOG_MESSAGE_FORMAT, LOG_TIME_FORMAT


class _ColourFormatter(logging.Formatter):
    """Formatter that adds colors to levelname only for console output."""

    COLOURS = {"DEBUG": 37, "INFO": 36, "WARNING": 33, "ERROR": 31, "CRITICAL": 41}
    RESET = "\033[0m"

    def format(self, record):
        # Save original levelname
        original_levelname = record.levelname
        # Add color only for formatting
        colour_code = self.COLOURS.get(record.levelname, "")
        if colour_code:
            record.levelname = f"\033[{colour_code}m{record.levelname}{self.RESET}"
        result = super().format(record=record)
        # Restore original levelname
        record.levelname = original_levelname
        return result


def configure_logging(
    *,
    level: str = "INFO",
    logfile_path: Optional[str] = None,
    enable_console: bool = True,
) -> None:
    """Initialise the *root* logger exactly once.

    Arguments
    ---------
    level         : Root log-level (e.g. "DEBUG", "INFO").
    logfile_path  : Path of the session-wide log file.  If None → default to 'logs/test_<timestamp>.log'.
    enable_console: If True a colourised StreamHandler is attached to stdout.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:  # Already configured?  Then do nothing.
        return

    root_logger.setLevel(level.upper())
    # Create plain formatter for file output
    plain_formatter = logging.Formatter(fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_TIME_FORMAT)

    # Ensure logs directory exists
    logs_dir = Path(LOG_DIR)
    logs_dir.mkdir(exist_ok=True)

    if not logfile_path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logfile_path = logs_dir / f"test_{timestamp}.log"  # type: ignore

    if enable_console:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(
            fmt=_ColourFormatter(fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_TIME_FORMAT)
        )
        root_logger.addHandler(hdlr=console_handler)

    file_handler = RotatingFileHandler(
        filename=str(object=logfile_path),
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt=plain_formatter)
    root_logger.addHandler(hdlr=file_handler)

    logging.captureWarnings(capture=True)
