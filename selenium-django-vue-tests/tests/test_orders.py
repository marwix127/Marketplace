from pages.orders_page import OrdersPage


def test_new_user_has_no_orders(driver, base_url, logged_in):
    assert OrdersPage(driver, base_url).open().is_empty()


def test_order_details_show_purchased_items(driver, base_url, api, logged_in, product):
    api.add_to_cart(logged_in["access"], product["id"], quantity=3)
    api.checkout(logged_in["access"])

    orders = OrdersPage(driver, base_url).open()

    assert orders.first_order_total() == "37.50€"
    assert orders.first_order_items() == [(product["title"], "x3")]
