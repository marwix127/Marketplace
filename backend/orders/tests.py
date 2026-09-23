from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from products.models import Product
from .models import Order, OrderItem

User = get_user_model()

LIST_URL = "/api/orders/"


def detail_url(pk):
    return f"/api/orders/{pk}/"


def create_order(user, title="Lámpara", price="10.50", quantity=2):
    price = Decimal(price)
    order = Order.objects.create(user=user, total_price=price * quantity)
    OrderItem.objects.create(
        order=order,
        product_title=title,
        product_price=price,
        quantity=quantity,
        subtotal=price * quantity,
    )
    return order


class OrderTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="ana@example.com", username="ana")
        cls.other = User.objects.create_user(email="luis@example.com", username="luis")
        cls.order = create_order(cls.user)
        cls.other_order = create_order(cls.other, title="Taza", price="3.00", quantity=1)

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_orders_require_authentication(self):
        self.client.force_authenticate(None)

        self.assertEqual(self.client.get(LIST_URL).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.get(detail_url(self.order.pk)).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_only_returns_own_orders(self):
        r = self.client.get(LIST_URL)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual([o["id"] for o in r.data], [self.order.id])

    def test_list_is_newest_first(self):
        older = create_order(self.user)
        Order.objects.filter(pk=older.pk).update(created_at=timezone.now() - timedelta(days=1))

        r = self.client.get(LIST_URL)

        self.assertEqual([o["id"] for o in r.data], [self.order.id, older.id])

    def test_retrieve_own_order_includes_items(self):
        r = self.client.get(detail_url(self.order.pk))

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["total_price"], "21.00")
        self.assertEqual(r.data["status"], "completed")
        self.assertEqual(len(r.data["items"]), 1)
        item = r.data["items"][0]
        self.assertEqual(
            (item["product_title"], item["product_price"], item["quantity"], item["subtotal"]),
            ("Lámpara", "10.50", 2, "21.00"),
        )

    def test_cannot_retrieve_another_users_order(self):
        r = self.client.get(detail_url(self.other_order.pk))

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_orders_are_read_only(self):
        self.assertEqual(self.client.post(LIST_URL, {}, format="json").status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.patch(detail_url(self.order.pk), {"status": "cancelled"}, format="json").status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(detail_url(self.order.pk)).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())


class OrderSnapshotTests(APITestCase):
    def test_order_keeps_product_data_after_product_changes(self):
        buyer = User.objects.create_user(email="ana@example.com", username="ana")
        seller = User.objects.create_user(email="tienda@example.com", username="tienda")
        product = Product.objects.create(owner=seller, title="Lámpara", price=Decimal("10.50"))
        cart = Cart.objects.create(user=buyer)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        self.client.force_authenticate(buyer)
        order_id = self.client.post("/api/cart/checkout/").data["id"]

        # The seller changes the price and then deletes the product
        product.title = "Lámpara nueva"
        product.price = Decimal("99.00")
        product.save()
        product.delete()

        r = self.client.get(detail_url(order_id))

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["total_price"], "21.00")
        item = r.data["items"][0]
        self.assertEqual((item["product_title"], item["product_price"]), ("Lámpara", "10.50"))
