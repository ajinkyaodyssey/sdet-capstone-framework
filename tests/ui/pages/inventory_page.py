from typing import TYPE_CHECKING, Self

from playwright.sync_api import expect

from tests.ui.pages.base_page import BasePage

if TYPE_CHECKING:
    from tests.ui.pages.cart_page import CartPage


class InventoryPage(BasePage):
    PATH = "/inventory.html"

    _TITLE = ".title"
    _ITEM_NAME = ".inventory_item_name"
    _CART_LINK = ".shopping_cart_link"
    _CART_BADGE = ".shopping_cart_badge"
    _SORT_DROPDOWN = ".product_sort_container"

    def expect_loaded(self) -> Self:
        expect(self.page.locator(self._TITLE)).to_have_text("Products")
        return self

    def get_item_names(self) -> list[str]:
        return self.page.locator(self._ITEM_NAME).all_inner_texts()

    def add_item(self, item_name: str) -> Self:
        slug = self.item_slug(item_name)
        self.page.click(f"#add-to-cart-{slug}")
        return self

    def remove_item(self, item_name: str) -> Self:
        slug = self.item_slug(item_name)
        self.page.click(f"#remove-{slug}")
        return self

    def expect_cart_count(self, count: int) -> Self:
        badge = self.page.locator(self._CART_BADGE)
        if count == 0:
            expect(badge).to_have_count(0)
        else:
            expect(badge).to_have_text(str(count))
        return self

    def sort_by(self, option: str) -> Self:
        self.page.select_option(self._SORT_DROPDOWN, option)
        return self

    def open_cart(self) -> "CartPage":
        self.page.click(self._CART_LINK)
        from tests.ui.pages.cart_page import CartPage

        return CartPage(self.page, self.base_url)