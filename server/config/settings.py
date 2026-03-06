import os

from server.utils.logger import get_logger

_logger = get_logger(__name__)

STORAGE_BASE_PATH = "/storage"
ASSETS_BASE_PATH = "/assets"


def _get_required_env(key: str) -> str:
    """Fetch a mandatory environment variable; raise loudly if absent."""
    value = os.environ.get(key)
    if not value:
        _logger.error("Required environment variable '%s' is not set.", key)
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set."
        )
    return value


class AppSettings:
    """
    Application-wide configuration parsed exclusively from environment
    variables. No secrets are ever hard-coded in this file.
    """

    def __init__(self) -> None:
        self.database_url: str = _get_required_env("DATABASE_URL")
        self.app_secret_key: str = _get_required_env("APP_SECRET_KEY")
        self.storage_base_path: str = os.environ.get(
            "STORAGE_BASE_PATH", STORAGE_BASE_PATH
        )
        self.log_level: str = os.environ.get("LOG_LEVEL", "INFO").upper()


def get_settings() -> AppSettings:
    """Return a fresh AppSettings instance (fail-fast on missing vars)."""
    try:
        return AppSettings()
    except EnvironmentError:
        _logger.critical(
            "Application cannot start — required environment variables are missing."
        )
        raise
