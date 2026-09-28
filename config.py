import yaml
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Load .env automatically when the module is imported
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and a YAML config file.
    """

    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    DATE_FORMAT: str = Field("%Y-%m-%d %H:%M:%S", env="DATE_FORMAT")
    CONFIG_PATH: Path = Field(Path("config.yaml"))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("LOG_LEVEL")
    def _validate_log_level(cls, v: str) -> str:
        allowed = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
        if v.upper() not in allowed:
            raise ValueError(f"Invalid LOG_LEVEL: {v}")
        return v.upper()


def load_yaml_config(path: Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    path: Path
        Path to the YAML file.

    Returns
    -------
    dict
        Parsed configuration.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}