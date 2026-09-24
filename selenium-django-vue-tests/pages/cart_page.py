from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class CartPage(BasePage):
    PATH = "/cart"

    ITEM = (By.CLASS_NAME, "cart-item")
    ITEM_TITLE = (By.CSS_SELECTOR, ".cart-item h3")
    EMPTY_MSG = (By.CLASS_NAME, "empty-cart")
    TOTAL = (By.CSS_SELECTOR, ".summary-row.total strong")
    CHECKOUT_BTN = (By.CLASS_NAME, "btn-checkout")
    CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Vaciar carrito']")

    @staticmethod
    def _item(title):
        return f"//div[contains(@class, 'cart-item')][.//h3[normalize-space()='{title}']]"

    def open(self):
        super().open()
        self.wait_loaded()
        return self

    def wait_loaded(self):
        self.wait.until(
            EC.any_of(EC.visibility_of_element_located(self.ITEM), EC.visibility_of_element_located(self.EMPTY_MSG)),
            "Cart did not finish loading",
        )

    def item_titles(self):
        return [element.text for element in self.find_all(self.ITEM_TITLE)]

    def quantity(self, title):
        return self.find((By.XPATH, f"{self._item(title)}//input")).get_attribute("value")

    def increase_quantity(self, title):
        self.click((By.XPATH, f"{self._item(title)}//button[normalize-space()='+']"))

    def remove(self, title):
        self.click((By.XPATH, f"{self._item(title)}//button[contains(@class, 'btn-remove')]"))
        self.wait_until_gone((By.XPATH, self._item(title)))

    def clear(self):
        self.click(self.CLEAR_BTN)
        self.wait.until(EC.alert_is_present(), "Confirmation dialog did not appear").accept()

    def total(self):
        return self.text_of(self.TOTAL)

    def wait_for_total(self, total):
        self.wait_for_text(self.TOTAL, total)

    def is_empty(self):
        return self.find(self.EMPTY_MSG).is_displayed()

    def checkout(self):
        self.click(self.CHECKOUT_BTN)
