from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    # Locators
    PRODUCTS_GRID = (By.CLASS_NAME, "products-grid")
    PRODUCT_CARD = (By.CLASS_NAME, "product-card")
    PRODUCT_TITLE = (By.TAG_NAME, "h3")
    ADD_TO_CART_BTN = (By.CLASS_NAME, "btn-add-to-cart")
    HERO_SECTION = (By.CLASS_NAME, "hero-section")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    CART_LINK = (By.CSS_SELECTOR, "a[href='/cart']")
    
    def get_products(self):
        # Wait until at least one product card is present
        self.find_element(self.PRODUCT_CARD) 
        return self.find_elements(self.PRODUCT_CARD)

    def get_product_titles(self):
        products = self.get_products()
        return [p.find_element(*self.PRODUCT_TITLE).text for p in products]

    def add_first_product_to_cart(self):
        products = self.get_products()
        if products:
            # Encuentra el botón dentro de la primera tarjeta
            btn = products[0].find_element(*self.ADD_TO_CART_BTN)
            btn.click()
            return True
        return False

    def go_to_login(self):
        # Asumiendo que hay un link en el navbar
        # Si no hay navbar definido en App.vue, podríamos navegar directamente
        self.driver.get(f"{self.driver.current_url.rstrip('/')}/login")

    def go_to_cart(self):
        self.driver.get(f"{self.driver.current_url.rstrip('/')}/cart")
