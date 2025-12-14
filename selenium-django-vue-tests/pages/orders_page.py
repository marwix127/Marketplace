from selenium.webdriver.common.by import By
from .base_page import BasePage

class OrdersPage(BasePage):
    ORDERS_LIST = (By.CSS_SELECTOR, ".orders-list")
    ORDER_CARD = (By.CSS_SELECTOR, ".order-card")
    EMPTY_ORDERS_MSG = (By.CSS_SELECTOR, ".empty-orders")
    ORDER_ID = (By.CSS_SELECTOR, ".order-info h3")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".order-total")
    ORDER_STATUS = (By.CSS_SELECTOR, ".order-status")
    
    def get_orders(self):
        # Simply find elements, wait implicitly if needed or explicitly
        # We wait for the list container first to ensure page loaded
        self.find_element(self.ORDERS_LIST, timeout=5)
        
        # Then get items
        return self.find_elements(self.ORDER_CARD)

    def get_first_order_id(self):
        orders = self.get_orders()
        if orders:
            return orders[0].find_element(*self.ORDER_ID).text
        return None
        
    def get_first_order_total(self):
        orders = self.get_orders()
        if orders:
            text = orders[0].find_element(*self.ORDER_TOTAL).text
            # "100.00€"
            return float(text.replace('€', '').strip())
        return 0.0
