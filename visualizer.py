import logging
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt

log = logging.getLogger(__name__)

def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def plot_level_distribution(level_counts: Dict[str, int], output_path: Path) -> None:
    """
    Create a bar chart of log levels.

    Parameters
    ----------
    level_counts: Dict[str, int]
        Mapping from log level to occurrence count.
    output_path: Path
        Destination PNG file.
    """
    log.info("Generating level distribution chart at %s", output_path)
    _ensure_dir(output_path)

    levels = list(level_counts.keys())
    counts = [level_counts[l] for l in levels]

    plt.figure(figsize=(8, 4))
    plt.bar(levels, counts, color='skyblue')
    plt.title("Log Level Distribution")
    plt.xlabel("Level")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    log.debug("Level chart saved.")


def plot_message_timeline(messages_per_bucket: Dict[str, int], output_path: Path) -> None:
    """
    Create a line chart of messages over time.

    Parameters
    ----------
    messages_per_bucket: Dict[str, int]
        Mapping from time bucket string to message count.
    output_path: Path
        Destination PNG file.
    """
    log.info("Generating timeline chart at %s", output_path)
    _ensure_dir(output_path)

    times = list(messages_per_bucket.keys())
    counts = [messages_per_bucket[t] for t in times]

    plt.figure(figsize=(10, 4))
    plt.plot(times, counts, marker='o', linestyle='-', color='steelblue')
    plt.title("Log Messages Over Time")
    plt.xlabel("Time")
    plt.ylabel("Number of Messages")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    log.debug("Timeline chart saved.")