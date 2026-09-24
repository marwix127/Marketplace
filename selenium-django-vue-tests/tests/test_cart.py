from pages.cart_page import CartPage
from pages.home_page import HomePage


def test_add_product_to_cart(driver, base_url, logged_in, product):
    home = HomePage(driver, base_url).open()
    home.add_to_cart(product["title"])
    home.wait_for_toast(f"{product['title']} añadido al carrito")
    home.wait_for_cart_count(1)

    cart = CartPage(driver, base_url).open()
    assert cart.item_titles() == [product["title"]]
    assert cart.quantity(product["title"]) == "1"
    assert cart.total() == "12.50€"


def test_adding_same_product_twice_increments_quantity(driver, base_url, logged_in, product):
    home = HomePage(driver, base_url).open()
    home.add_to_cart(product["title"])
    home.wait_for_cart_count(1)
    home.add_to_cart(product["title"])
    home.wait_for_cart_count(2)

    cart = CartPage(driver, base_url).open()
    assert cart.item_titles() == [product["title"]]
    assert cart.quantity(product["title"]) == "2"
    assert cart.total() == "25.00€"


def test_increase_quantity_updates_total(driver, base_url, api, logged_in, product):
    api.add_to_cart(logged_in["access"], product["id"])

    cart = CartPage(driver, base_url).open()
    cart.increase_quantity(product["title"])

    cart.wait_for_total("25.00€")
    assert cart.quantity(product["title"]) == "2"


def test_remove_product_from_cart(driver, base_url, api, logged_in, product):
    api.add_to_cart(logged_in["access"], product["id"])

    cart = CartPage(driver, base_url).open()
    cart.remove(product["title"])

    assert cart.is_empty()


def test_clear_cart(driver, base_url, api, logged_in, product):
    api.add_to_cart(logged_in["access"], product["id"], quantity=3)

    cart = CartPage(driver, base_url).open()
    cart.clear()

    assert cart.is_empty()
