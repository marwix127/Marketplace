from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order, OrderItem
from products.models import Product
from .models import Cart, CartItem

User = get_user_model()


class CartTestCase(APITestCase):
    """Fixtures: two buyers, two products from a third user, and `user` logged in."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="ana@example.com", username="ana")
        cls.other = User.objects.create_user(email="luis@example.com", username="luis")
        seller = User.objects.create_user(email="tienda@example.com", username="tienda")
        cls.lamp = Product.objects.create(owner=seller, title="Lámpara", price=Decimal("10.50"))
        cls.mug = Product.objects.create(owner=seller, title="Taza", price=Decimal("3.00"))

    def setUp(self):
        self.client.force_authenticate(self.user)

    def post(self, action, data=None):
        return self.client.post(f"/api/cart/{action}/", data or {}, format="json")

    def add_to_cart(self, user, product, quantity):
        cart, created = Cart.objects.get_or_create(user=user)
        return CartItem.objects.create(cart=cart, product=product, quantity=quantity)


class CartAccessTests(CartTestCase):
    def test_cart_requires_authentication(self):
        self.client.force_authenticate(None)

        for method, url in [
            ("get", "/api/cart/my_cart/"),
            ("post", "/api/cart/add_item/"),
            ("post", "/api/cart/checkout/"),
        ]:
            with self.subTest(url=url):
                r = getattr(self.client, method)(url)
                self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_my_cart_is_created_empty_on_first_access(self):
        r = self.client.get("/api/cart/my_cart/")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["items"], [])
        self.assertEqual(r.data["total_price"], 0)
        self.assertTrue(Cart.objects.filter(user=self.user).exists())

    def test_my_cart_returns_items_with_subtotals_and_total(self):
        self.add_to_cart(self.user, self.lamp, 2)
        self.add_to_cart(self.user, self.mug, 1)

        r = self.client.get("/api/cart/my_cart/")

        subtotals = {item["product"]["title"]: item["subtotal"] for item in r.data["items"]}
        self.assertEqual(subtotals, {"Lámpara": 21.0, "Taza": 3.0})
        self.assertEqual(r.data["total_price"], 24.0)

    def test_generic_cart_endpoints_are_not_exposed(self):
        cart = Cart.objects.create(user=self.user)
        not_exposed = (status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertIn(self.client.post("/api/cart/", {}, format="json").status_code, not_exposed)
        self.assertIn(self.client.delete(f"/api/cart/{cart.pk}/").status_code, not_exposed)
        self.assertTrue(Cart.objects.filter(pk=cart.pk).exists())


class AddItemTests(CartTestCase):
    def test_add_new_product_returns_201(self):
        r = self.post("add_item", {"product_id": self.lamp.id, "quantity": 2})

        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.data)
        self.assertEqual(r.data["quantity"], 2)
        self.assertEqual(r.data["subtotal"], 21.0)

    def test_quantity_defaults_to_one(self):
        r = self.post("add_item", {"product_id": self.lamp.id})

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data["quantity"], 1)

    def test_adding_same_product_again_increments_quantity(self):
        self.post("add_item", {"product_id": self.lamp.id, "quantity": 2})

        r = self.post("add_item", {"product_id": self.lamp.id, "quantity": 3})

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["quantity"], 5)
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 1)

    def test_unknown_product_returns_404(self):
        r = self.post("add_item", {"product_id": 9999})

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_quantity_returns_400(self):
        for quantity in [0, -1, "abc"]:
            with self.subTest(quantity=quantity):
                r = self.post("add_item", {"product_id": self.lamp.id, "quantity": quantity})
                self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CartItem.objects.exists())

    def test_non_numeric_product_id_returns_404(self):
        r = self.post("add_item", {"product_id": "abc"})

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_null_quantity_returns_400(self):
        r = self.post("add_item", {"product_id": self.lamp.id, "quantity": None})

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateRemoveClearTests(CartTestCase):
    def setUp(self):
        super().setUp()
        self.item = self.add_to_cart(self.user, self.lamp, 2)
        self.other_item = self.add_to_cart(self.other, self.mug, 4)

    def test_update_item_sets_quantity(self):
        r = self.post("update_item", {"item_id": self.item.id, "quantity": 7})

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 7)

    def test_update_item_with_invalid_quantity_returns_400(self):
        for quantity in [0, -3, "abc", None]:
            with self.subTest(quantity=quantity):
                r = self.post("update_item", {"item_id": self.item.id, "quantity": quantity})
                self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 2)

    def test_update_missing_item_returns_404(self):
        r = self.post("update_item", {"item_id": 9999, "quantity": 1})

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_item(self):
        r = self.post("remove_item", {"item_id": self.item.id})

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertFalse(CartItem.objects.filter(pk=self.item.pk).exists())

    def test_remove_missing_item_returns_404(self):
        r = self.post("remove_item", {"item_id": 9999})

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_numeric_item_id_returns_404(self):
        update = self.post("update_item", {"item_id": "abc", "quantity": 1})
        remove = self.post("remove_item", {"item_id": "abc"})

        self.assertEqual(update.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(remove.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_touch_another_users_items(self):
        update = self.post("update_item", {"item_id": self.other_item.id, "quantity": 1})
        remove = self.post("remove_item", {"item_id": self.other_item.id})

        self.assertEqual(update.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(remove.status_code, status.HTTP_404_NOT_FOUND)
        self.other_item.refresh_from_db()
        self.assertEqual(self.other_item.quantity, 4)

    def test_clear_only_empties_own_cart(self):
        r = self.post("clear")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertFalse(CartItem.objects.filter(cart__user=self.user).exists())
        self.assertTrue(CartItem.objects.filter(pk=self.other_item.pk).exists())


class CheckoutTests(CartTestCase):
    def setUp(self):
        super().setUp()
        self.add_to_cart(self.user, self.lamp, 2)
        self.add_to_cart(self.user, self.mug, 1)

    def test_checkout_creates_order_and_empties_cart(self):
        r = self.post("checkout")

        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.data)
        self.assertEqual(Decimal(r.data["total_price"]), Decimal("24.00"))
        items = {item["product_title"]: item for item in r.data["items"]}
        self.assertEqual(items["Lámpara"]["quantity"], 2)
        self.assertEqual(Decimal(items["Lámpara"]["subtotal"]), Decimal("21.00"))
        self.assertEqual(Decimal(items["Taza"]["product_price"]), Decimal("3.00"))
        self.assertEqual(Order.objects.get().user, self.user)
        self.assertFalse(CartItem.objects.filter(cart__user=self.user).exists())

    def test_checkout_with_empty_cart_returns_400(self):
        CartItem.objects.all().delete()

        r = self.post("checkout")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Order.objects.exists())

    def test_checkout_does_not_touch_other_carts(self):
        other_item = self.add_to_cart(self.other, self.mug, 4)

        self.post("checkout")

        self.assertTrue(CartItem.objects.filter(pk=other_item.pk).exists())
        self.assertFalse(Order.objects.filter(user=self.other).exists())

    def test_checkout_rolls_back_on_failure(self):
        with patch.object(OrderItem.objects, "bulk_create", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                self.post("checkout")

        # Nothing persisted, cart intact
        self.assertFalse(Order.objects.exists())
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 2)
