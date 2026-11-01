from typing import TYPE_CHECKING, Self

from playwright.sync_api import expect

from tests.ui.pages.base_page import BasePage

if TYPE_CHECKING:
    from tests.ui.pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    PATH = "/"

    _USERNAME = "#user-name"
    _PASSWORD = "#password"
    _LOGIN_BUTTON = "#login-button"
    _ERROR = '[data-test="error"]'

    def expect_loaded(self) -> Self:
        expect(self.page.locator(self._LOGIN_BUTTON)).to_be_visible()
        return self

    def enter_username(self, username: str) -> Self:
        self.page.fill(self._USERNAME, username)
        return self

    def enter_password(self, password: str) -> Self:
        self.page.fill(self._PASSWORD, password)
        return self

    def click_login(self) -> None:
        self.page.click(self._LOGIN_BUTTON)

    def login(self, username: str, password: str) -> "InventoryPage":
        self.enter_username(username).enter_password(password).click_login()
        from tests.ui.pages.inventory_page import InventoryPage

        return InventoryPage(self.page, self.base_url)

    def login_expecting_failure(self, username: str, password: str) -> Self:
        self.enter_username(username).enter_password(password).click_login()
        return self

    def get_error_message(self) -> str:
        return self.page.locator(self._ERROR).inner_text()

    def expect_error_contains(self, text: str) -> Self:
        expect(self.page.locator(self._ERROR)).to_contain_text(text)
        return self