from factories import user_data
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage


def test_register_new_user(driver, base_url):
    new_user = user_data()

    register_page = RegisterPage(driver, base_url).open()
    register_page.register(**new_user)
    register_page.wait_for_toast("Cuenta creada correctamente")

    # The new account can log in
    LoginPage(driver, base_url).open().login(new_user["email"], new_user["password"])
    home = HomePage(driver, base_url)
    home.wait_for_path("/")
    assert home.greeting() == f"Hola, {new_user['username']}"


def test_register_rejects_weak_password(driver, base_url):
    new_user = {**user_data(), "password": "12345"}

    register_page = RegisterPage(driver, base_url).open()
    register_page.register(**new_user)

    assert "This password is too short" in register_page.error_message()


def test_login_valid_credentials(driver, base_url, user):
    LoginPage(driver, base_url).open().login(user["email"], user["password"])

    home = HomePage(driver, base_url)
    home.wait_for_path("/")
    assert home.greeting() == f"Hola, {user['username']}"


def test_login_invalid_credentials(driver, base_url, user):
    login_page = LoginPage(driver, base_url).open()
    login_page.login(user["email"], "wrong-password")

    assert login_page.error_message() == "No active account found with the given credentials"
    assert driver.current_url == f"{base_url}/login"
    assert driver.execute_script("return localStorage.getItem('access')") is None


def test_logout(driver, base_url, logged_in):
    home = HomePage(driver, base_url).open()
    assert home.greeting() == f"Hola, {logged_in['username']}"

    home.logout()

    assert home.is_logged_out()
    assert driver.execute_script("return localStorage.getItem('access')") is None
