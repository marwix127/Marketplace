import uuid

PASSWORD = "E2e-Str0ng-pass!"


def unique(prefix):
    """A name that won't collide with data from other tests or previous runs."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def user_data():
    username = unique("e2e")
    return {"email": f"{username}@example.com", "username": username, "password": PASSWORD}
