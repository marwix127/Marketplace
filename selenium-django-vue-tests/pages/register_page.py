from selenium.webdriver.common.by import By

from .base_page import BasePage


class RegisterPage(BasePage):
    PATH = "/register"

    EMAIL_INPUT = (By.ID, "email")
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-error")

    def register(self, email, username, password):
        self.type(self.EMAIL_INPUT, email)
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def error_message(self):
        return self.text_of(self.ERROR_ALERT)
