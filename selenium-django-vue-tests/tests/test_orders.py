import pytest
import time
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.orders_page import OrdersPage

def test_view_orders(driver, base_url, created_user):
    # 1. Login
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    home_page.go_to_login()

    login_page = LoginPage(driver)
    login_page.login(created_user["email"], created_user["password"])
    time.sleep(1)

    # 2. Add product to cart
    home_page.add_first_product_to_cart()
    time.sleep(1)

    # 3. Go to cart and checkout
    home_page.go_to_cart()
    cart_page = CartPage(driver)
    cart_page.checkout()
    time.sleep(3)

    # 4. Now view orders (should be on orders page after checkout)
    assert "/orders" in driver.current_url

    orders_page = OrdersPage(driver)

    # Wait for loading
    loading_locator = (By.CLASS_NAME, "loading")
    time.sleep(0.5)
    if orders_page.is_visible(loading_locator):
        orders_page.wait_for_invisibility(loading_locator, timeout=5)

    # Check orders exist
    if orders_page.is_visible(orders_page.EMPTY_ORDERS_MSG):
        pytest.fail("No orders found after checkout")

    orders = orders_page.get_orders()
    assert len(orders) > 0

    # Verify order details (e.g., total)
    order_total = orders_page.get_first_order_total()
    assert order_total > 0