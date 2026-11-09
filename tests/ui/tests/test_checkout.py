from config.config import ui_config
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.inventory_page import InventoryPage
from tests.ui.pages.cart_page import CartPage
from tests.ui.pages.checkout_page import CheckoutPage
from playwright.sync_api import expect
import re

def page_after_login(page):
    return LoginPage(page, ui_config.BASE_URL).navigate().expect_loaded().login(ui_config.USERNAME, ui_config.PASSWORD)

def test_validate_successful_purchase(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    checkout = cart.checkout()
    checkout.expect_loaded().fill_shipping_info(checkout._FIRST_NAME, checkout._LAST_NAME, checkout._POSTAL_CODE).click_continue().expect_overview_loaded().finish().expect_order_complete()

def test_missing_first_name_displays_error(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    checkout = cart.checkout()
    checkout.expect_loaded().fill_shipping_info("", checkout._LAST_NAME, checkout._POSTAL_CODE).click_continue().expect_error_contains("Error: First Name is required")

def test_missing_postal_code_displays_error(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    checkout = cart.checkout()
    checkout.expect_loaded().fill_shipping_info(checkout._FIRST_NAME, checkout._LAST_NAME, "").click_continue().expect_error_contains("Error: Postal Code is required")

def test_back_home_returns_to_inventory_page(page):
    inventory = page_after_login(page)
    cart = inventory.add_item("Sauce Labs Backpack").open_cart()
    checkout = cart.checkout()
    checkout.expect_loaded().fill_shipping_info(checkout._FIRST_NAME, checkout._LAST_NAME, checkout._POSTAL_CODE).click_continue().expect_overview_loaded().finish().expect_order_complete()
    inventory = checkout.back_home()
    expect(inventory.page).to_have_url(re.compile("/inventory.html"))