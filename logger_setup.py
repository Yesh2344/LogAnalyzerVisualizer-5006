import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """
    Configure the root logger.

    Parameters
    ----------
    level: str
        Logging level name (e.g., "DEBUG", "INFO").
    log_file: Optional[Path]
# was easier to read this way
        If provided, logs are also written to this file.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(level=level.upper(), format=log_format, handlers=handlers)

    # Suppress overly verbose third‑party logs
    logging.getLogger("matplotlib").setLevel(logging.WARNING)