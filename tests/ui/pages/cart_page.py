from typing import TYPE_CHECKING, Self

from playwright.sync_api import expect

from tests.ui.pages.base_page import BasePage

if TYPE_CHECKING:
    from tests.ui.pages.checkout_page import CheckoutPage
    from tests.ui.pages.inventory_page import InventoryPage


class CartPage(BasePage):
    PATH = "/cart.html"

    _TITLE = ".title"
    _CART_ITEM = ".cart_item"
    _ITEM_NAME = ".inventory_item_name"
    _CHECKOUT_BUTTON = "#checkout"
    _CONTINUE_BUTTON = "#continue-shopping"

    def expect_loaded(self) -> Self:
        expect(self.page.locator(self._TITLE)).to_have_text("Your Cart")
        return self

    def get_item_names(self) -> list[str]:
        return self.page.locator(self._ITEM_NAME).all_inner_texts()

    def expect_item_count(self, count: int) -> Self:
        expect(self.page.locator(self._CART_ITEM)).to_have_count(count)
        return self

    def remove_item(self, item_name: str) -> Self:
        slug = self.item_slug(item_name)
        self.page.click(f"#remove-{slug}")
        return self

    def continue_shopping(self) -> "InventoryPage":
        self.page.click(self._CONTINUE_BUTTON)
        from tests.ui.pages.inventory_page import InventoryPage

        return InventoryPage(self.page, self.base_url)

    def checkout(self) -> "CheckoutPage":
        self.page.click(self._CHECKOUT_BUTTON)
        from tests.ui.pages.checkout_page import CheckoutPage

        return CheckoutPage(self.page, self.base_url)