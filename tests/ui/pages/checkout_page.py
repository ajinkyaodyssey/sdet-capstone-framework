from typing import TYPE_CHECKING, Self

from playwright.sync_api import expect

from tests.ui.pages.base_page import BasePage

if TYPE_CHECKING:
    from tests.ui.pages.inventory_page import InventoryPage


class CheckoutPage(BasePage):
    PATH = "/checkout-step-one.html"

    _TITLE = ".title"
    _FIRST_NAME = "#first-name"
    _LAST_NAME = "#last-name"
    _POSTAL_CODE = "#postal-code"
    _CONTINUE_BUTTON = "#continue"
    _FINISH_BUTTON = "#finish"
    _BACK_HOME_BUTTON = "#back-to-products"
    _COMPLETE_HEADER = ".complete-header"
    _ERROR = '[data-test="error"]'

    def expect_loaded(self) -> Self:
        title = self.page.locator(self._TITLE)
        expect(title).to_have_text("Checkout: Your Information")
        return self

    def fill_shipping_info(self, first: str, last: str, postal: str) -> Self:
        self.page.fill(self._FIRST_NAME, first)
        self.page.fill(self._LAST_NAME, last)
        self.page.fill(self._POSTAL_CODE, postal)
        return self

    def click_continue(self) -> Self:
        self.page.click(self._CONTINUE_BUTTON)
        return self

    def expect_overview_loaded(self) -> Self:
        title = self.page.locator(self._TITLE)
        expect(title).to_have_text("Checkout: Overview")
        return self

    def finish(self) -> Self:
        self.page.click(self._FINISH_BUTTON)
        return self

    def expect_order_complete(self) -> Self:
        header = self.page.locator(self._COMPLETE_HEADER)
        expect(header).to_have_text("Thank you for your order!")
        return self

    def expect_error_contains(self, text: str) -> Self:
        expect(self.page.locator(self._ERROR)).to_contain_text(text)
        return self

    def back_home(self) -> "InventoryPage":
        self.page.click(self._BACK_HOME_BUTTON)
        from tests.ui.pages.inventory_page import InventoryPage

        return InventoryPage(self.page, self.base_url)