from config.config import ui_config


def test_login_page_fixture_is_ready(login_page):
    inventory = login_page.login(ui_config.USERNAME, ui_config.PASSWORD)

    inventory.expect_loaded()


def test_inventory_page_fixture_is_already_logged_in(inventory_page):
    inventory_page.add_item("Sauce Labs Backpack").expect_cart_count(1)
