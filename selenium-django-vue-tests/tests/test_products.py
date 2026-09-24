from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage


def test_view_product_details(driver, base_url, product):
    HomePage(driver, base_url).open().open_details(product["title"])

    detail = ProductDetailPage(driver, base_url)
    detail.wait_for_path(f"/product/{product['id']}")
    assert detail.title() == product["title"]
    assert detail.description() == product["description"]
    assert detail.price() == "Precio: 12.50 €"


def test_add_to_cart_from_product_detail(driver, base_url, logged_in, product):
    # Regression: this button used to call a wrong endpoint and still show a success message
    detail = ProductDetailPage(driver, base_url).open_product(product["id"])
    detail.add_to_cart()
    detail.wait_for_toast(f"{product['title']} añadido al carrito")

    assert CartPage(driver, base_url).open().item_titles() == [product["title"]]
