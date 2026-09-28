import argparse
import logging
from pathlib import Path

from config import Settings, load_yaml_config
from logger_setup import setup_logging
from analyzer import analyze_log, LogStats
from visualizer import plot_level_distribution, plot_message_timeline

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a log file and generate visual reports."
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        required=True,
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./output"),
        help="Directory where PNG charts will be stored."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Settings().CONFIG_PATH,
        help="Path to a custom YAML configuration file."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings()
    setup_logging(settings.LOG_LEVEL)

    logging.info("Loading configuration from %s", args.config)
    yaml_cfg = load_yaml_config(args.config)

    time_bucket = yaml_cfg.get("analysis", {}).get("time_bucket", "hour")
    viz_cfg = yaml_cfg.get("visualization", {})

    # Run analysis
    stats: LogStats = analyze_log(
        file_path=args.log_file,
        date_format=settings.DATE_FORMAT,
        time_bucket=time_bucket,
    )

    # Generate visualizations
    output_dir: Path = args.output_dir
    level_chart_path = output_dir / viz_cfg.get("level_chart", "log_levels.png")
    timeline_chart_path = output_dir / viz_cfg.get("timeline_chart", "log_timeline.png")

    plot_level_distribution(stats.level_counts, level_chart_path)
    plot_message_timeline(stats.messages_per_bucket, timeline_chart_path)

    logging.info("All reports generated in %s", output_dir)


if __name__ == "__main__":
    main()