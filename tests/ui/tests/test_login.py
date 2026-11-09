from config.config import ui_config
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.inventory_page import InventoryPage
from playwright.sync_api import expect


def open_login_page(page):
    return LoginPage(page, ui_config.BASE_URL).navigate().expect_loaded()


def test_valid_user_lands_on_inventory_page(page):
    inventory = open_login_page(page).login(ui_config.USERNAME, ui_config.PASSWORD)
    inventory.expect_loaded()
    expect(page).to_have_url(f"{ui_config.BASE_URL}{InventoryPage.PATH}")
    

def test_wrong_password_shows_error(page):
    login_page = open_login_page(page).login_expecting_failure(ui_config.USERNAME, "WrongPassword")
    login_page.expect_error_contains("Username and password do not match")
    

def test_empty_username_shows_username_is_required(page):
    login_page = open_login_page(page).login_expecting_failure("", ui_config.PASSWORD).expect_error_contains("Username is required")


def test_empty_password_shows_password_is_required(page):
    login_page = open_login_page(page).login_expecting_failure(ui_config.USERNAME, "").expect_error_contains("Password is required")


def test_locked_out_user_shows_locked_out(page):
    login_page = open_login_page(page).login_expecting_failure("locked_out_user", ui_config.PASSWORD).expect_error_contains("Sorry, this user has been locked out.")


def test_non_existing_user_shows_do_not_match_error(page):
    login_page = open_login_page(page).login_expecting_failure("error_user", "WrongPassword").expect_error_contains("do not match")
