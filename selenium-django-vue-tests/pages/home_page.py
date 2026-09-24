from selenium.webdriver.common.by import By

from .base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    GREETING = (By.CSS_SELECTOR, ".nav-user .nav-link")
    LOGOUT_BTN = (By.CSS_SELECTOR, "button.logout")
    LOGIN_LINK = (By.CSS_SELECTOR, ".nav-menu a[href='/login']")
    CART_BADGE = (By.CLASS_NAME, "cart-badge")

    @staticmethod
    def _card(title):
        return f"//div[contains(@class, 'product-card')][.//h3[normalize-space()='{title}']]"

    def add_to_cart(self, title):
        self.click((By.XPATH, f"{self._card(title)}//button[contains(@class, 'btn-add-to-cart')]"))

    def open_details(self, title):
        self.click((By.XPATH, f"{self._card(title)}//a[contains(@class, 'btn-details')]"))

    def greeting(self):
        return self.text_of(self.GREETING)

    def logout(self):
        self.click(self.LOGOUT_BTN)

    def is_logged_out(self):
        return self.find(self.LOGIN_LINK).is_displayed()

    def wait_for_cart_count(self, count):
        self.wait_for_text(self.CART_BADGE, f"({count})")
