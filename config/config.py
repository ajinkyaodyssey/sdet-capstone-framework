# config/config.py
#
# WHY THIS FILE EXISTS:
# If os.getenv("APP_URL") is scattered across 30 test files,
# changing the variable name means updating 30 files.
# This module reads ALL environment variables in ONE place.
# Every other file imports from here — never calls os.getenv directly.
#
# HOW IT WORKS:
# python-dotenv reads .env file → loads into os.environ
# os.getenv() reads from os.environ
# In CI: GitHub Actions secrets inject variables directly
# Same code works locally and in CI

import os
from pathlib import Path
from dotenv import load_dotenv

# Find project root regardless of where pytest is run from
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Load .env file silently — ignored if file does not exist
# In CI, variables come from GitHub Actions secrets instead
load_dotenv(ENV_FILE)


def _require(key: str) -> str:
    """
    Get a required environment variable.
    Raises clear error if missing — better than cryptic
    AttributeError or KeyError later in the test.
    """
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"\n\nRequired environment variable '{key}' is not set.\n"
            f"Add it to your .env file: {ENV_FILE}\n"
            f"See .env.example for the complete list.\n"
        )
    return value


def _optional(key: str, default: str = "") -> str:
    """Get an optional environment variable with a safe default."""
    return os.getenv(key, default)


# =============================================
# UI / BROWSER CONFIGURATION
# =============================================

class UIConfig:
    """
    Configuration for Playwright UI tests.
    Reads from environment so the same tests can run
    against staging or production by changing one env var.
    """
    BASE_URL: str = _optional(
        "APP_URL",
        "https://www.saucedemo.com"
    )
    USERNAME: str = _optional(
        "APP_USERNAME",
        "standard_user"
    )
    PASSWORD: str = _optional(
        "APP_PASSWORD",
        "secret_sauce"
    )
    HEADLESS: bool = _optional(
        "HEADLESS", "true"
    ).lower() == "true"

    SCREENSHOT_DIR: str = _optional(
        "SCREENSHOT_DIR",
        "reports/screenshots"
    )


# =============================================
# API CONFIGURATION
# =============================================

class APIConfig:
    """
    Configuration for API tests.
    API_KEY is required — tests skip if not set.
    """
    BASE_URL: str = _optional(
        "API_BASE_URL",
        "https://reqres.in/api"
    )
    API_KEY: str = _optional("REQRES_API_KEY", "")

    @property
    def has_key(self) -> bool:
        """True if API key is configured."""
        return bool(self.API_KEY)


# =============================================
# REPORTING CONFIGURATION
# =============================================

class ReportConfig:
    REPORT_DIR: str = _optional("REPORT_DIR", "reports")
    SCREENSHOT_DIR: str = _optional(
        "SCREENSHOT_DIR",
        "reports/screenshots"
    )


# =============================================
# ENVIRONMENT INFO
# =============================================

class EnvConfig:
    ENV: str = _optional("TEST_ENV", "staging")

    @property
    def is_staging(self) -> bool:
        return self.ENV == "staging"

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"


# Singleton instances — import these in test files
# from config.config import ui_config, api_config
ui_config = UIConfig()
api_config = APIConfig()
report_config = ReportConfig()
env_config = EnvConfig()
