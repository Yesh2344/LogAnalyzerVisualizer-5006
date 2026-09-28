import logging
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from utils import read_file_lines, parse_log_line

log = logging.getLogger(__name__)

@dataclass
class LogStats:
    """
    Container for aggregated log statistics.
    """
    level_counts: Dict[str, int]
    messages_per_bucket: Dict[str, int]  # bucket -> count (hourly or daily)


def _bucket_timestamp(ts: datetime, bucket: str) -> str:
    """
    Convert a datetime to a string bucket.

    Parameters
    ----------
    ts: datetime
    bucket: str
        Either "hour" or "day".

    Returns
    -------
    str
        Formatted bucket string.
    """
    if bucket == "hour":
        return ts.strftime("%Y-%m-%d %H:00")
    elif bucket == "day":
        return ts.strftime("%Y-%m-%d")
    else:
        raise ValueError(f"Unsupported bucket: {bucket}")


def analyze_log(
    file_path: Path,
    date_format: str,
    time_bucket: str = "hour"
) -> LogStats:
    """
    Parse a log file and compute statistics.

    Parameters
    ----------
    file_path: Path
        Path to the log file.
    date_format: str
        Datetime format used in the log file.
    time_bucket: str
        Granularity for time‑based aggregation ("hour" or "day").

    Returns
    -------
    LogStats
        Aggregated statistics.
    """
    log.info("Starting analysis of %s", file_path)
    lines = read_file_lines(file_path)

    level_counter: Counter[str] = Counter()
    time_counter: defaultdict[str, int] = defaultdict(int)

    for idx, line in enumerate(lines, start=1):
        parsed = parse_log_line(line, date_format)
        if not parsed:
            log.debug("Skipping unparsable line %d: %s", idx, line)
            continue
        ts, level, _ = parsed
        level_counter[level] += 1
        bucket = _bucket_timestamp(ts, time_bucket)
        time_counter[bucket] += 1

    stats = LogStats(
        level_counts=dict(level_counter),
        messages_per_bucket=dict(sorted(time_counter.items()))
    )
    log.info("Analysis complete: %d levels, %d time buckets", len(stats.level_counts), len(stats.messages_per_bucket))
    return stats