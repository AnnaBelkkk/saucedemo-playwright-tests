from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com/"

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USER = "locked_out_user"


# Вспомогательная функция для выполнения шага авторизации с заданными логином и паролем
def perform_login(page: Page, username: str, password: str) -> None:
    page.goto(BASE_URL)
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


# Тест проверяет успешный логин стандартного пользователя и переход на страницу со списком товаров
def test_successful_login(page: Page) -> None:
    perform_login(page, VALID_USER, VALID_PASSWORD)

    page.wait_for_url("**/inventory.html")
    assert page.is_visible(".inventory_list")


# Тест проверяет, что заблокированный пользователь не может войти и получает сообщение об ошибке
def test_locked_out_user_login(page: Page) -> None:
    perform_login(page, LOCKED_USER, VALID_PASSWORD)

    error = page.locator("[data-test='error']")
    assert error.is_visible()
    assert "locked out" in error.inner_text().lower()


# Тест проверяет, что при неверных учётных данных отображается ошибка о неправильном логине или пароле
def test_invalid_credentials_login(page: Page) -> None:
    perform_login(page, "some_invalid_user", "wrong_password")

    error = page.locator("[data-test='error']")
    assert error.is_visible()
    assert "username and password do not match" in error.inner_text().lower()

