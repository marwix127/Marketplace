from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=None):
        timeout = timeout if timeout else self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            print(f"Element not found: {locator}")
            return None

    def find_elements(self, locator, timeout=None):
        timeout = timeout if timeout else self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def click(self, locator):
        element = self.find_element(locator)
        if element:
            element.click()
        else:
            raise Exception(f"Cannot click element: {locator}")

    def type_text(self, locator, text):
        element = self.find_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
        else:
             raise Exception(f"Cannot type in element: {locator}")

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text if element else ""

    def is_visible(self, locator):
        try:
            element = self.find_element(locator)
            return element.is_displayed() if element else False
        except:
            return False

    def wait_for_invisibility(self, locator, timeout=None):
        timeout = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

