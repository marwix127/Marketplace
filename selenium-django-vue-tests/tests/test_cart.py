import pytest
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage

def test_add_product_to_cart(driver, base_url, created_user):
    # 1. Login first (as per app requirement)
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    home_page.go_to_login()
    
    login_page = LoginPage(driver)
    login_page.login(created_user["email"], created_user["password"])
    time.sleep(1) # wait for redirect

    # 2. Add product
    assert home_page.add_first_product_to_cart() == True
    time.sleep(1) # wait for toast/api

    # 3. Go to cart
    home_page.go_to_cart()
    
    # 4. Verify item in cart
    cart_page = CartPage(driver)
    items = cart_page.get_cart_items()
    assert len(items) > 0
    
    # Cleanup: clear cart
    cart_page.clear_cart()

def test_cart_total_calculation(driver, base_url, created_user):
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
    
    # 3. Check total in cart
    home_page.go_to_cart()
    cart_page = CartPage(driver)
    
    total = cart_page.get_total_price()
    assert total > 0

    # Cleanup
    cart_page.clear_cart()

def test_remove_product_from_cart(driver, base_url, created_user):
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
    
    # Verify item added
    items = cart_page.get_cart_items()
    assert len(items) > 0
    
    # 4. Remove product (assuming there's a remove button)
    # Need to check cart_page for remove method
    cart_page.remove_first_item()
    time.sleep(1)
    
    # Verify cart is empty or item removed
    items_after = cart_page.get_cart_items()
    assert len(items_after) == 0
