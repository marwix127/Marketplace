from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()

PASSWORD = "Sup3r-secret-pw"


class RegisterTests(APITestCase):
    url = "/api/users/register/"

    def test_register_creates_user_with_hashed_password(self):
        r = self.client.post(self.url, {"email": "ana@example.com", "username": "ana", "password": PASSWORD}, format="json")

        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.data)
        # The password is never echoed back
        self.assertEqual(r.data, {"email": "ana@example.com", "username": "ana"})
        user = User.objects.get(email="ana@example.com")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))

    def test_register_rejects_weak_password(self):
        r = self.client.post(self.url, {"email": "ana@example.com", "username": "ana", "password": "12345"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", r.data)
        self.assertFalse(User.objects.exists())

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(email="ana@example.com", username="ana")

        r = self.client.post(self.url, {"email": "ana@example.com", "username": "otra", "password": PASSWORD}, format="json")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", r.data)

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user(email="ana@example.com", username="ana")

        r = self.client.post(self.url, {"email": "otra@example.com", "username": "ana", "password": PASSWORD}, format="json")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", r.data)

    def test_register_requires_all_fields(self):
        r = self.client.post(self.url, {}, format="json")

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(r.data), {"email", "username", "password"})


class LoginTests(APITestCase):
    url = "/api/users/login/"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="ana@example.com", username="ana", password=PASSWORD)

    def test_login_with_email_returns_tokens_and_user(self):
        r = self.client.post(self.url, {"email": "ana@example.com", "password": PASSWORD}, format="json")

        self.assertEqual(r.status_code, status.HTTP_200_OK, r.data)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        self.assertEqual(r.data["user"], {"id": self.user.id, "username": "ana", "email": "ana@example.com"})

    def test_access_token_includes_username_and_email(self):
        r = self.client.post(self.url, {"email": "ana@example.com", "password": PASSWORD}, format="json")

        token = AccessToken(r.data["access"])
        self.assertEqual(token["username"], "ana")
        self.assertEqual(token["email"], "ana@example.com")

    def test_login_with_wrong_password_returns_401(self):
        r = self.client.post(self.url, {"email": "ana@example.com", "password": "wrong-password"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", r.data)


class MeAndRefreshTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="ana@example.com", username="ana")

    def test_me_returns_authenticated_user(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        r = self.client.get("/api/users/me/")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, {"id": self.user.id, "email": "ana@example.com", "username": "ana"})

    def test_me_requires_authentication(self):
        r = self.client.get("/api/users/me/")

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_rejects_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer not-a-valid-token")

        r = self.client.get("/api/users/me/")

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_returns_working_access_token(self):
        refresh = RefreshToken.for_user(self.user)

        r = self.client.post("/api/users/refresh/", {"refresh": str(refresh)}, format="json")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {r.data['access']}")
        self.assertEqual(self.client.get("/api/users/me/").status_code, status.HTTP_200_OK)

    def test_refresh_with_invalid_token_returns_401(self):
        r = self.client.post("/api/users/refresh/", {"refresh": "not-a-valid-token"}, format="json")

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
