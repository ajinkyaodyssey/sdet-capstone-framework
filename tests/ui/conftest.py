import logging
import re
from pathlib import Path

import pytest

from config.config import ui_config
from tests.ui.pages.inventory_page import InventoryPage
from tests.ui.pages.login_page import LoginPage

log = logging.getLogger(__name__)

SCREENSHOT_DIR = Path("reports/screenshots")


@pytest.fixture(scope="session")
def auth_state_path(browser, tmp_path_factory):
    state_file = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context()
    page = context.new_page()
    (
        LoginPage(page, ui_config.BASE_URL)
        .navigate()
        .login(ui_config.USERNAME, ui_config.PASSWORD)
        .expect_loaded()
    )
    context.storage_state(path=str(state_file))
    context.close()
    return str(state_file)


@pytest.fixture
def logged_in_page(browser, auth_state_path):
    context = browser.new_context(storage_state=auth_state_path)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def login_page(page):
    return LoginPage(page, ui_config.BASE_URL).navigate().expect_loaded()


@pytest.fixture
def inventory_page(logged_in_page):
    return InventoryPage(logged_in_page, ui_config.BASE_URL).navigate().expect_loaded()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    for fixture_name in ("page", "logged_in_page"):
        page = item.funcargs.get(fixture_name)
        if page is None:
            continue
        safe_name = re.sub(r"[^\w.-]", "_", item.name)
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        path = SCREENSHOT_DIR / f"FAIL_{safe_name}.png"
        try:
            page.screenshot(path=str(path), full_page=True)
            log.info("Saved failure screenshot: %s", path)
        except Exception as error:
            log.warning("Could not take screenshot: %s", error)
