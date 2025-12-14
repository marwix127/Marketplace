import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.register_page import RegisterPage
import time
import random

def test_register_new_user(driver, base_url):
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    
    # Navigate to register (assuming link exists on login page or home)
    # If not, go direct
    driver.get(f"{base_url}/register")
    
    register_page = RegisterPage(driver)
    # Randomize user to avoid unique constraint errors if re-running
    rnd = random.randint(1000, 9999)
    email = f"testuser{rnd}@example.com"
    user = f"testuser{rnd}"
    pwd = "StrongPassword123!"
    
    register_page.register(email, user, pwd)
    
    # Check success - maybe redirects to login or shows success message
    # Looking at Register.vue: shows success toast/alert? "¡Cuenta creada correctamente!"
    # Assume it stays on page or we can check alert
    time.sleep(2) # Wait for api
    
    # Verify success message or redirection
    # Register.vue clears inputs on success
    # Let's try to login with this new user immediately to verify
    driver.get(f"{base_url}/login")
    login_page = LoginPage(driver)
    login_page.login(email, pwd)
    time.sleep(2)
    assert driver.current_url.rstrip('/') == base_url.rstrip('/')

def test_login_valid_credentials(driver, base_url, created_user):
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    home_page.go_to_login()
    
    login_page = LoginPage(driver)
    
    # Try to login
    login_page.login(created_user["email"], created_user["password"])
    
    # Wait for redirect
    time.sleep(2) 
    
    # Debug: Print current URL if failed
    if driver.current_url.rstrip('/') != base_url.rstrip('/'):
        print(f"Login failed. Still on: {driver.current_url}")
        # Check for error message
        err = login_page.get_error_message()
        print(f"Error message: {err}")
    
    assert driver.current_url.rstrip('/') == base_url.rstrip('/')
    
    # Ideally verify "Logout" button exists or username is displayed

def test_login_invalid_credentials(driver, base_url):
    home_page = HomePage(driver)
    home_page.open_url(base_url)
    home_page.go_to_login()
    
    login_page = LoginPage(driver)
    login_page.login("wrong@email.com", "wrongpass")
    
    time.sleep(1)
    # Verify error message
    error_msg = login_page.get_error_message()
    assert error_msg != ""

