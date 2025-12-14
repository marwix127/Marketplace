import pytest
import time
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.login_page import LoginPage

def test_view_product_details(driver, base_url, created_user):
    # 1. Login
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    home_page.go_to_login()

    login_page = LoginPage(driver)
    login_page.login(created_user["email"], created_user["password"])
    time.sleep(1)

    # 2. Click on first product to view details
    products = home_page.get_products()
    if products:
        # Click on "Ver detalles" button
        details_btn = products[0].find_element(By.CLASS_NAME, "btn-details")
        details_btn.click()
        time.sleep(2)

        # Check if on product detail page (URL contains /product/)
        assert "/product/" in driver.current_url

        # Verify product details are shown (title is h2)
        title = driver.find_element(By.TAG_NAME, "h2").text
        assert title != ""  # Basic check

        # Check description
        description = driver.find_element(By.CSS_SELECTOR, "p.mb-2").text
        assert description != ""

        # Check price (the p with class mb-3)
        price_p = driver.find_element(By.CSS_SELECTOR, "p.mb-3")
        assert "€" in price_p.text
    else:
        pytest.fail("No products available to view details")