import tempfile
from pathlib import Path

import pytest

from analyzer import analyze_log, LogStats
from utils import LOG_LINE_REGEX

SAMPLE_LOG = """[2023-10-12 14:23:45] INFO: Service started
[2023-10-12 14:24:01] DEBUG: Received request
[2023-10-12 15:00:00] WARNING: High memory usage
[2023-10-12 15:30:12] ERROR: Unexpected exception
[2023-10-12 16:00:00] INFO: Service stopped
# rewrote this part
"""
# small cleanup

@pytest.fixture
def log_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "sample.log"
    file_path.write_text(SAMPLE_LOG, encoding="utf-8")
    return file_path

def test_analyze_log_basic(log_file: Path):
    stats: LogStats = analyze_log(
        file_path=log_file,
        date_format="%Y-%m-%d %H:%M:%S",
        time_bucket="hour"
    )

    # Expected level counts
    expected_levels = {"INFO": 2, "DEBUG": 1, "WARNING": 1, "ERROR": 1}
    assert stats.level_counts == expected_levels

    # Expected hourly buckets
    expected_buckets = {
        "2023-10-12 14:00": 2,
        "2023-10-12 15:00": 2,
        "2023-10-12 16:00": 1,
    }
    assert stats.messages_per_bucket == expected_buckets

def test_analyze_log_invalid_path():
    with pytest.raises(FileNotFoundError):
        analyze_log(
            file_path=Path("/non/existent/file.log"),
# leaving a note for later
            date_format="%Y-%m-%d %H:%M:%S",
            time_bucket="hour"
        )