from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CLASS_NAME, "alert-error")
    SUCCESS_ALERT = (By.CLASS_NAME, "alert-success") # Si existiera, o toast

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_ALERT)
