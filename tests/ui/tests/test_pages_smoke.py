from config.config import ui_config
from tests.ui.pages.login_page import LoginPage


def open_login_page(page) -> LoginPage:
    return LoginPage(page, ui_config.BASE_URL).navigate().expect_loaded()


def test_valid_login_lands_on_inventory(page):
    inventory = open_login_page(page).login(
        ui_config.USERNAME,
        ui_config.PASSWORD,
    )
    inventory.expect_loaded()
    inventory.expect_url_contains("/inventory")


def test_wrong_password_shows_error(page):
    login_page = open_login_page(page)
    login_page.login_expecting_failure(ui_config.USERNAME, "wrong_password")
    login_page.expect_error_contains("do not match")


def test_full_purchase_chain(page):
    (
        open_login_page(page)
        .login(ui_config.USERNAME, ui_config.PASSWORD)
        .expect_loaded()
        .add_item("Sauce Labs Backpack")
        .expect_cart_count(1)
        .open_cart()
        .expect_loaded()
        .expect_item_count(1)
        .checkout()
        .expect_loaded()
        .fill_shipping_info("Ajinkya", "Tester", "411001")
        .click_continue()
        .expect_overview_loaded()
        .finish()
        .expect_order_complete()
    )