from config.config import ui_config
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.inventory_page import InventoryPage
from tests.ui.pages.cart_page import CartPage
from playwright.sync_api import expect

def page_after_login(page):
    return LoginPage(page, ui_config.BASE_URL).navigate().expect_loaded().login(ui_config.USERNAME, ui_config.PASSWORD)

def test_added_item_appears_in_cart_by_name(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    cart.expect_loaded()
    expect(cart.page.locator(cart._ITEM_NAME)).to_have_text("Sauce Labs Backpack")


def test_two_added_items_give_a_cart_item_count_of_2(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").add_item("Sauce Labs Bike Light").open_cart()
    cart.expect_loaded()
    expect(cart.page.locator(cart._CART_ITEM)).to_have_count(2)


def test_removing_the_only_item_leaves_the_cart_empty(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    cart.expect_loaded()
    cart.remove_item("Sauce Labs Backpack").expect_item_count(0)
    
def test_continue_shopping_returns_to_the_inventory_page(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    cart.expect_loaded()
    inventory = cart.continue_shopping()
    inventory.expect_loaded()
    inventory.expect_url_contains("/inventory.html")
