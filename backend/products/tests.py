import os
import shutil
import tempfile
from decimal import Decimal
from io import BytesIO
from unittest import expectedFailure

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product

User = get_user_model()

LIST_URL = "/api/products/"


def detail_url(pk):
    return f"/api/products/{pk}/"


def make_image(name="foto.png"):
    buffer = BytesIO()
    Image.new("RGB", (10, 10), "red").save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


class ProductTestCase(APITestCase):
    """Fixtures: a product owned by `owner` and a second user who doesn't own it."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(email="ana@example.com", username="ana")
        cls.other = User.objects.create_user(email="luis@example.com", username="luis")
        cls.product = Product.objects.create(owner=cls.owner, title="Lámpara", price=Decimal("19.99"))


class ProductReadTests(ProductTestCase):
    def test_list_is_public(self):
        r = self.client.get(LIST_URL)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["title"], "Lámpara")
        self.assertEqual(r.data[0]["owner"], "ana")

    def test_detail_is_public(self):
        r = self.client.get(detail_url(self.product.pk))

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["price"], "19.99")

    def test_detail_of_missing_product_returns_404(self):
        r = self.client.get(detail_url(9999))

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class ProductCreateTests(ProductTestCase):
    def test_create_requires_authentication(self):
        r = self.client.post(LIST_URL, {"title": "Silla", "price": "30.00"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Product.objects.filter(title="Silla").exists())

    def test_create_sets_owner_to_current_user(self):
        self.client.force_authenticate(self.owner)

        # `owner` in the payload is ignored
        r = self.client.post(LIST_URL, {"title": "Silla", "price": "30.00", "owner": "luis"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.data)
        self.assertEqual(r.data["owner"], "ana")
        self.assertEqual(Product.objects.get(pk=r.data["id"]).owner, self.owner)

    def test_create_requires_title_and_price(self):
        self.client.force_authenticate(self.owner)

        r = self.client.post(LIST_URL, {"description": "Sin título ni precio"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", r.data)
        self.assertIn("price", r.data)

    @expectedFailure  # BUG: no price validation, a negative price is accepted (201)
    def test_create_rejects_negative_price(self):
        self.client.force_authenticate(self.owner)

        r = self.client.post(LIST_URL, {"title": "Silla", "price": "-5.00"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class ProductOwnershipTests(ProductTestCase):
    def test_owner_can_update(self):
        self.client.force_authenticate(self.owner)

        r = self.client.patch(detail_url(self.product.pk), {"price": "15.00"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_200_OK, r.data)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal("15.00"))

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.owner)

        r = self.client.delete(detail_url(self.product.pk))

        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_other_user_cannot_update(self):
        self.client.force_authenticate(self.other)

        r = self.client.patch(detail_url(self.product.pk), {"price": "1.00"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal("19.99"))

    def test_other_user_cannot_delete(self):
        self.client.force_authenticate(self.other)

        r = self.client.delete(detail_url(self.product.pk))

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_anonymous_cannot_update_or_delete(self):
        self.assertEqual(self.client.patch(detail_url(self.product.pk), {"price": "1.00"}, format="json").status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.delete(detail_url(self.product.pk)).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())


class ProductImageTests(ProductTestCase):
    def setUp(self):
        # Uploaded files go to a temporary MEDIA_ROOT, never to backend/media
        media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media_root, ignore_errors=True)
        override = self.settings(MEDIA_ROOT=media_root)
        override.enable()
        self.addCleanup(override.disable)
        self.client.force_authenticate(self.owner)

    def test_create_with_image(self):
        r = self.client.post(LIST_URL, {"title": "Foto", "price": "5.00", "image": make_image()}, format="multipart")

        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.data)
        product = Product.objects.get(pk=r.data["id"])
        self.assertTrue(product.image.name.startswith("product_images/"))
        self.assertTrue(os.path.exists(product.image.path))
        self.assertTrue(r.data["image"].endswith(f"/media/{product.image.name}"))

    def test_create_rejects_file_that_is_not_an_image(self):
        fake = SimpleUploadedFile("foto.png", b"not an image", content_type="image/png")

        r = self.client.post(LIST_URL, {"title": "Foto", "price": "5.00", "image": fake}, format="multipart")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", r.data)
