import pytest
import time
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.orders_page import OrdersPage

def test_checkout_process(driver, base_url, created_user):
    # 1. Login
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    home_page.go_to_login()
    
    login_page = LoginPage(driver)
    login_page.login(created_user["email"], created_user["password"])
    time.sleep(1)

    # 2. Add product
    home_page.add_first_product_to_cart()
    time.sleep(1)
    
    # 3. Go to cart
    home_page.go_to_cart()
    cart_page = CartPage(driver)
    
    # Check we have items
    assert len(cart_page.get_cart_items()) > 0
    total_cart = cart_page.get_total_price()
    
    # 4. Checkout
    cart_page.checkout()
    
    # Wait for redirection to Orders
    time.sleep(3)
    assert "/orders" in driver.current_url
    
    # 5. Verify Order
    orders_page = OrdersPage(driver)
    
    # Wait for loading to finish
    loading_locator = (By.CLASS_NAME, "loading")
    # Tiny sleep to ensure Vue mounted and started loading
    time.sleep(0.5) 
    
    if orders_page.is_visible(loading_locator):
        if not orders_page.wait_for_invisibility(loading_locator, timeout=5):
            pytest.fail("Loading indicator stuck!")

    # Check validation states
    if orders_page.is_visible(orders_page.EMPTY_ORDERS_MSG):
        pytest.fail("Checkout redirected to orders, but order list is empty.")

    orders = orders_page.get_orders()


    
    assert len(orders) > 0, "No orders found (List container not found)"
    
    # Verify latest order (assuming first in list is latest) has same total
    order_total = orders_page.get_first_order_total()
    
    assert order_total == total_cart
