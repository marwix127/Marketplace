from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-error")

    def login(self, email, password):
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def error_message(self):
        return self.text_of(self.ERROR_ALERT)
