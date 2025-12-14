from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegisterPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_ALERT = (By.CLASS_NAME, "alert-success") # Assuming success shows an alert or redirects

    def register(self, email, username, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)
