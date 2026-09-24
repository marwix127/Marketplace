from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Common helpers. Every lookup waits explicitly and fails with a clear message instead of returning None."""

    PATH = "/"
    TIMEOUT = 10

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self):
        self.driver.get(f"{self.base_url}{self.PATH}")
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator), f"Element not visible: {locator}")

    def find_all(self, locator):
        # No waiting here: call it once the page has reached the expected state
        return self.driver.find_elements(*locator)

    def click(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator), f"Element not found: {locator}")
        # Centre it so fixed elements (toasts, Vue DevTools button) don't cover it
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.element_to_be_clickable(locator), f"Element not clickable: {locator}").click()

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def wait_for_text(self, locator, text):
        self.wait.until(EC.text_to_be_present_in_element(locator, text), f"Text {text!r} not found in {locator}")

    def wait_until_gone(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator), f"Element still visible: {locator}")

    def wait_for_path(self, path):
        url = f"{self.base_url}{path}"
        self.wait.until(EC.url_to_be(url), f"Expected URL {url}, got {self.driver.current_url}")

    def wait_for_toast(self, text):
        """Wait for a toast notification containing `text` and return its full message."""
        return self.text_of((By.XPATH, f"//p[contains(@class, 'toast-message')][contains(., '{text}')]"))
