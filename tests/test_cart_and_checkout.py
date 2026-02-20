from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com/"

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


# Вспомогательная функция: логинится под стандартным пользователем и дожидается загрузки страницы товаров
def login_as_standard_user(page: Page) -> None:
    page.goto(BASE_URL)
    page.fill("#user-name", VALID_USER)
    page.fill("#password", VALID_PASSWORD)
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")


# Тест проверяет добавление товара в корзину и отображение его в корзине
def test_add_item_to_cart(page: Page) -> None:
    login_as_standard_user(page)

    backpack_btn = page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
    backpack_btn.click()

    badge = page.locator(".shopping_cart_badge")
    assert badge.is_visible()
    assert badge.inner_text() == "1"

    page.click(".shopping_cart_link")
    cart_item = page.locator(".cart_item")
    assert cart_item.count() == 1
    assert "Sauce Labs Backpack" in cart_item.nth(0).inner_text()


# Тест проверяет, что можно удалить один из ранее добавленных товаров из корзины
def test_remove_item_from_cart(page: Page) -> None:
    login_as_standard_user(page)

    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()

    page.click(".shopping_cart_link")
    cart_items = page.locator(".cart_item")
    assert cart_items.count() == 2

    page.locator("[data-test='remove-sauce-labs-backpack']").click()

    cart_items_after = page.locator(".cart_item")
    assert cart_items_after.count() == 1
    remaining_text = cart_items_after.nth(0).inner_text()
    assert "Sauce Labs Bike Light" in remaining_text


# Тест проверяет полный сценpytest --tracing=onполнение формы и завершение покупки
def test_full_checkout_flow(page: Page) -> None:
    login_as_standard_user(page)

    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.click(".shopping_cart_link")

    page.locator("[data-test='checkout']").click()

    page.fill("[data-test='firstName']", "Anna")
    page.fill("[data-test='lastName']", "Belk")
    page.fill("[data-test='postalCode']", "12345")
    page.locator("[data-test='continue']").click()

    page.locator("[data-test='finish']").click()

    header = page.locator(".complete-header")
    assert header.is_visible()
    assert "THANK YOU FOR YOUR ORDER" in header.inner_text().upper()

