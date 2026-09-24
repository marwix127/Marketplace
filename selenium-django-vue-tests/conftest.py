import os
from pathlib import Path

import pytest
import pytest_html
import requests
from dotenv import load_dotenv
from selenium import webdriver

from api_client import ApiClient
from factories import unique, user_data

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:5173").rstrip("/")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes")

SCREENSHOTS_DIR = Path(__file__).parent / "reports" / "screenshots"


@pytest.fixture(scope="session", autouse=True)
def servers_are_up():
    """Fail fast with a clear message if the backend or the frontend isn't running."""
    for name, url in [("backend", f"{API_URL}/products/"), ("frontend", BASE_URL)]:
        try:
            requests.get(url, timeout=5)
        except requests.ConnectionError:
            pytest.exit(f"The {name} is not reachable at {url}. Start it before running the E2E tests.", returncode=1)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api():
    return ApiClient(API_URL)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # Selenium Manager downloads the matching chromedriver automatically
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def user(api):
    """A brand-new user for each test, so every test starts with an empty cart and no orders."""
    data = user_data()
    api.register(**data)
    return data


@pytest.fixture(scope="session")
def seller(api):
    data = user_data()
    api.register(**data)
    return data


@pytest.fixture
def product(api, seller):
    """A product created through the API and deleted after the test."""
    token = api.login(seller["email"], seller["password"])["access"]
    created = api.create_product(token, title=unique("Producto"), price="12.50", description="Creado por los tests E2E")
    yield created
    token = api.login(seller["email"], seller["password"])["access"]
    api.delete_product(token, created["id"])


@pytest.fixture
def logged_in(driver, api, user):
    """Log `user` in by storing API tokens the way the app does (the login form has its own tests).

    The session is picked up on the next page load. Returns the user data plus its `access` token.
    """
    session = api.login(user["email"], user["password"])
    driver.get(BASE_URL)
    driver.execute_script(
        """
        localStorage.setItem('access', arguments[0]);
        localStorage.setItem('refresh', arguments[1]);
        localStorage.setItem('username', arguments[2].username);
        localStorage.setItem('email', arguments[2].email);
        """,
        session["access"],
        session["refresh"],
        session["user"],
    )
    return {**user, "access": session["access"]}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, save a screenshot and the browser console, and attach them to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver")
    if report.when != "call" or not report.failed or driver is None:
        return

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    screenshot = SCREENSHOTS_DIR / f"{item.name}.png"
    driver.save_screenshot(str(screenshot))
    report.sections.append(("Screenshot", str(screenshot)))

    console = "\n".join(entry["message"] for entry in driver.get_log("browser"))
    if console:
        report.sections.append(("Browser console", console))

    report.extras = getattr(report, "extras", []) + [pytest_html.extras.png(driver.get_screenshot_as_base64())]
