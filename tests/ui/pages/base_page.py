import logging
import re
from typing import Self

from playwright.sync_api import Page, expect

log = logging.getLogger(__name__)


class BasePage:
    PATH = ""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate(self) -> Self:
        url = f"{self.base_url}{self.PATH}"
        log.info("Navigating to %s", url)
        self.page.goto(url)
        return self

    def expect_loaded(self) -> Self:
        raise NotImplementedError(
            f"{type(self).__name__} must implement expect_loaded()"
        )

    def get_title(self) -> str:
        return self.page.title()

    def expect_url_contains(self, fragment: str) -> Self:
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))
        return self

    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(
            path=f"reports/screenshots/{name}.png",
            full_page=True,
        )

    @staticmethod
    def item_slug(item_name: str) -> str:
        return item_name.lower().replace(" ", "-")