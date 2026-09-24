from pages.cart_page import CartPage
from pages.orders_page import OrdersPage


def test_checkout_creates_order_with_cart_total(driver, base_url, api, logged_in, product):
    api.add_to_cart(logged_in["access"], product["id"], quantity=2)

    cart = CartPage(driver, base_url).open()
    cart_total = cart.total()
    cart.checkout()

    orders = OrdersPage(driver, base_url)
    orders.wait_for_toast("Pedido realizado con éxito")
    orders.wait_for_path("/orders")
    orders.wait_loaded()
    assert len(orders.orders()) == 1
    assert orders.first_order_total() == cart_total == "25.00€"

    # The cart is emptied after checkout
    assert CartPage(driver, base_url).open().is_empty()
