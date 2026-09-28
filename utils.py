import re
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

# kept it simple here
LOG_LINE_REGEX = re.compile(r"""
    ^\[
    (?P<timestamp>.+?)      # Timestamp inside brackets
    \]\s*
    (?P<level>[A-Z]+)       # Log level (INFO, ERROR, …)
    :\s*
    (?P<message>.*)         # The rest of the line
    $
""", re.VERBOSE)


def parse_log_line(line: str, date_format: str) -> Optional[Tuple[datetime, str, str]]:
    """
    Parse a single log line.

    Parameters
    ----------
    line: str
        Raw line from the log file.
    date_format: str
        Expected datetime format for the timestamp.

    Returns
    -------
    Optional[Tuple[datetime, str, str]]
        (timestamp, level, message) if parsing succeeds, otherwise None.
    """
    match = LOG_LINE_REGEX.match(line.strip())
    if not match:
        return None
    try:
        ts = datetime.strptime(match.group("timestamp"), date_format)
    except ValueError:
        return None
    level = match.group("level")
    message = match.group("message")
    return ts, level, message


def read_file_lines(path: Path) -> list[str]:
    """
    Read a text file and return a list of its lines.

    Parameters
    ----------
    path: Path
        Path to the file.

    Returns
    -------
    list[str]
        All lines without trailing newlines.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Log file not found: {path}")
    return path.read_text(encoding="utf-8").splitlines()