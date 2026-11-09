from config.config import ui_config
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.inventory_page import InventoryPage
from playwright.sync_api import expect


def page_after_login(page):
    return LoginPage(page, ui_config.BASE_URL).navigate().expect_loaded().login(ui_config.USERNAME, ui_config.PASSWORD)


def test_inventory_page_contains_exactly_six_products(page):
    inventory = page_after_login(page)
    inventory.expect_loaded()
    assert inventory.page.locator(InventoryPage._ITEM_NAME).count() == 6


def test_adding_one_item_badge_shows_cart_badge_as_one(page):
    inventory = page_after_login(page)
    inventory.expect_loaded()
    inventory.add_item("Sauce Labs Backpack")
    inventory.expect_cart_count(1)


def test_adding_two_items_badge_shows_cart_badge_as_two(page):
    inventory = page_after_login(page)
    inventory.expect_loaded()
    inventory.add_item("Sauce Labs Backpack")
    inventory.add_item("Sauce Labs Bike Light")
    inventory.expect_cart_count(2)


def test_removing_item_makes_badge_disappear(page):
    inventory = page_after_login(page)
    inventory.expect_loaded()
    inventory.expect_cart_count(0)
    inventory.add_item("Sauce Labs Backpack")
    inventory.expect_cart_count(1)
    inventory.remove_item("Sauce Labs Backpack")
    inventory.expect_cart_count(0)


def test_validate_sorting_z_to_a(page):
    inventory = page_after_login(page)
    inventory.expect_loaded()
    item_names_before = sorted(inventory.get_item_names(), reverse = True)
    inventory.sort_by("za")
    item_names_after = inventory.get_item_names()
    assert item_names_before == item_names_after


def test_calidate_sorting_price_low_to_high(page):
    inventory = page_after_login(page)
    inventory.expect_loaded()
    item_prices_before = sorted(inventory.get_prices())
    inventory.sort_by("lohi")
    item_prices_after = inventory.get_prices()
    assert item_prices_before == item_prices_after
