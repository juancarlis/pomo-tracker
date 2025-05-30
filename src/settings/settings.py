from pathlib import Path
from typing import Optional

import yaml
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Represents the application settings using Pydantic's BaseSettings for
    automatic environment variable handling and data validation.
    """

    default_category: str = "Inbox"
    db_path: str = "~/.config/pomo-tracker/tasks.db"

    class Config:
        # If you want environment variables to override these fields, ensure
        # that their names match the field in uppercase (e.g., DEFAULT_CATEGORY, DB_PATH).
        # Example: `export DEFAULT_CATEGORY="Inbox"`

        env_prefix = (
            ""  # No prefix, so the env var name is EXACTLY the field name in uppercase
        )
        case_sensitive = False  # If True, env variables must match case exactly


def load_settings_from_yaml(
    yaml_file: Optional[str] = "~/.config/pomo-tracker/config.yaml",
) -> dict:
    """
    Loads settings from a YAML file and returns them as dictionary.
    If the file does not exist or is empty, returns an empty dictionary.

    Args:
        yaml_file (str): Path to the YAML configuration file.

    Returns:
        dict: A dictionary fo loaded settings (may be empty if file is missing).
    """

    if not yaml_file:
        return {}

    path_obj = Path(yaml_file).expanduser()
    if not path_obj.is_file():
        return {}

    with path_obj.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def init_settings(config_file: Optional[str] = None) -> AppSettings:
    """
    Initializes the application settings by mergin default values,
    values loaded from a YAML file, and environment variables.

    The priority is:
        1) Default values (harcoded in AppSettings)
        2) YAML file (if provided/found)
        3) Environment variables (highest priority)

    Args:
        config_file (str): Path to a YAML file. If None, uses a default location.

    Returns:
        AppSettings: An instance with merged settings.
    """

    data_from_yaml = load_settings_from_yaml(
        config_file or "~/.config/pomo-tracker/config.yaml"
    )

    # Pass the YAML data into AppSettings. BaseSettings will handle environment overrides automatically
    settings = AppSettings(**data_from_yaml)
    return settings


# Create singleton/global instance for ease import throught the app.
settings = init_settings()
