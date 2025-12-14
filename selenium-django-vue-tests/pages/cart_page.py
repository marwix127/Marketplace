from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart-item")
    EMPTY_CART_MSG = (By.CLASS_NAME, "empty-cart")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".summary-row.total strong")
    REMOVE_BTN = (By.CLASS_NAME, "btn-remove")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".quantity-controls input")
    CLEAR_CART_BTN = (By.XPATH, "//button[contains(text(), 'Vaciar carrito')]")
    CHECKOUT_BTN = (By.CLASS_NAME, "btn-checkout")

    def get_cart_items(self):
        return self.find_elements(self.CART_ITEMS)

    def is_cart_empty(self):
        return self.is_visible(self.EMPTY_CART_MSG)

    def get_total_price(self):
        text = self.get_text(self.TOTAL_PRICE)
        # text format: "100.00€" -> remove currency and parse
        return float(text.replace('€', '').strip())

    def remove_first_item(self):
        items = self.get_cart_items()
        if items:
            btn = items[0].find_element(*self.REMOVE_BTN)
            btn.click()

    def clear_cart(self):
        self.click(self.CLEAR_CART_BTN)
        # Confirm alert if present
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass
            
    def checkout(self):
        self.click(self.CHECKOUT_BTN)

