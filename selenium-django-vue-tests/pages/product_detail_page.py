from selenium.webdriver.common.by import By

from .base_page import BasePage


class ProductDetailPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".product-info h2")
    DESCRIPTION = (By.CSS_SELECTOR, ".product-info p.mb-2")
    PRICE = (By.CSS_SELECTOR, ".product-info p.mb-3")
    ADD_TO_CART_BTN = (By.XPATH, "//button[normalize-space()='Añadir al carrito']")

    def open_product(self, product_id):
        self.driver.get(f"{self.base_url}/product/{product_id}")
        return self

    def title(self):
        return self.text_of(self.TITLE)

    def description(self):
        return self.text_of(self.DESCRIPTION)

    def price(self):
        return self.text_of(self.PRICE)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)
