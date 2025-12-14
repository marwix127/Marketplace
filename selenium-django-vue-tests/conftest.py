import pytest
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:5173"

@pytest.fixture(scope="session")
def api_url():
    return "http://127.0.0.1:8000/api"

@pytest.fixture(scope="session")
def test_user_data():
    return {
        "email": "test_selenium_user@example.com",
        "username": "selenium_user",
        "password": "StrongPassword123!" 
    }

@pytest.fixture(scope="session")
def created_user(api_url, test_user_data):
    # Try to register the user
    try:
        requests.post(f"{api_url}/users/register/", json=test_user_data)
        # Verify it exists or was created (201 or 400 if exists)
        # If exists, we assume credentials match or we might fail login
    except:
        pass
    return test_user_data

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    # User requested to see the tests, so NO headless mode
    #options.add_argument("--headless") 
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    
    # Enable browser logging
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10) # Implicit wait for elements
    
    yield driver
    
    # Capture logs on exit
    for entry in driver.get_log('browser'):
        print(f"[BROWSER LOG] {entry}")

    driver.quit()
