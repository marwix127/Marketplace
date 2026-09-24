from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class OrdersPage(BasePage):
    PATH = "/orders"

    ORDER = (By.CLASS_NAME, "order-card")
    EMPTY_MSG = (By.CLASS_NAME, "empty-orders")
    FIRST_ORDER_HEADER = (By.CSS_SELECTOR, ".order-card:first-child .order-header")
    FIRST_ORDER_TOTAL = (By.CSS_SELECTOR, ".order-card:first-child .order-total")
    FIRST_ORDER_ITEMS = (By.CSS_SELECTOR, ".order-card:first-child .order-item")

    def open(self):
        super().open()
        self.wait_loaded()
        return self

    def wait_loaded(self):
        self.wait.until(
            EC.any_of(EC.visibility_of_element_located(self.ORDER), EC.visibility_of_element_located(self.EMPTY_MSG)),
            "Orders did not finish loading",
        )

    def orders(self):
        return self.find_all(self.ORDER)

    def is_empty(self):
        return self.find(self.EMPTY_MSG).is_displayed()

    def first_order_total(self):
        return self.text_of(self.FIRST_ORDER_TOTAL)

    def first_order_items(self):
        """Expand the most recent order and return its lines as (title, quantity) pairs."""
        self.click(self.FIRST_ORDER_HEADER)
        self.find(self.FIRST_ORDER_ITEMS)
        return [
            (item.find_element(By.CLASS_NAME, "item-title").text, item.find_element(By.CLASS_NAME, "item-quantity").text)
            for item in self.find_all(self.FIRST_ORDER_ITEMS)
        ]
