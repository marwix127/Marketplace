import requests


class ApiClient:
    """Thin wrapper around the backend API, used to prepare test data without going through the UI."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.http = requests.Session()

    def _request(self, method, path, token=None, **kwargs):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = self.http.request(method, f"{self.base_url}{path}", headers=headers, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else None

    def register(self, email, username, password):
        return self._request("POST", "/users/register/", json={"email": email, "username": username, "password": password})

    def login(self, email, password):
        """Returns {"access", "refresh", "user"}."""
        return self._request("POST", "/users/login/", json={"email": email, "password": password})

    def create_product(self, token, title, price, description=""):
        return self._request("POST", "/products/", token, json={"title": title, "price": price, "description": description})

    def delete_product(self, token, product_id):
        self._request("DELETE", f"/products/{product_id}/", token)

    def add_to_cart(self, token, product_id, quantity=1):
        return self._request("POST", "/cart/add_item/", token, json={"product_id": product_id, "quantity": quantity})

    def checkout(self, token):
        return self._request("POST", "/cart/checkout/", token)
