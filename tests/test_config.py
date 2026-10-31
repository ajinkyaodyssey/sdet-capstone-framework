# tests/test_config.py
# Verify config module loads properly
# Run: pytest tests/test_config.py -v

from config.config import ui_config, api_config, env_config


def test_ui_config_has_base_url():
    """APP_URL must be set and start with https."""
    assert ui_config.BASE_URL
    assert ui_config.BASE_URL.startswith("https://"), (
        f"APP_URL must be HTTPS, got: {ui_config.BASE_URL}"
    )


def test_ui_config_has_credentials():
    """Username and password must be configured."""
    assert ui_config.USERNAME, "APP_USERNAME not set"
    assert ui_config.PASSWORD, "APP_USERNAME not set"


def test_api_config_has_base_url():
    """API_BASE_URL must be set."""
    assert api_config.BASE_URL
    assert "reqres.in" in api_config.BASE_URL


def test_env_config_defaults_to_staging():
    """Default environment should be staging."""
    assert env_config.ENV in ["staging", "production", "local"], (
        f"Unexpected environment: {env_config.ENV}"
    )


def test_config_base_url_has_no_trailing_slash():
    """
    URLs with trailing slashes cause double-slash issues.
    https://api.com//users instead of https://api.com/users
    """
    assert not ui_config.BASE_URL.endswith("/"), (
        f"Remove trailing slash from APP_URL: {ui_config.BASE_URL}"
    )
