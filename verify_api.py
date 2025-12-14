import requests
import random

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("Testing API...")
    
    # 1. Register
    rnd = random.randint(10000, 99999)
    email = f"api_test_{rnd}@example.com"
    username = f"api_test_{rnd}"
    password = "password123"
    
    print(f"Registering user: {email}")
    try:
        r = requests.post(f"{BASE_URL}/users/register/", json={
            "email": email,
            "username": username,
            "password": password
        })
        print(f"Register Status: {r.status_code}")
        print(f"Register Response: {r.text}")
    except Exception as e:
        print(f"Register Failed: {e}")
        return

    # 2. Login
    print("Logging in...")
    try:
        r = requests.post(f"{BASE_URL}/users/login/", json={
            "email": email,
            "password": password
        })
        print(f"Login Status: {r.status_code}")
        print(f"Login Response: {r.text}")
        
        if r.status_code == 200:
            token = r.json()['access']
            print("Login Successful")
            
            # 3. Get Products
            print("Fetching products...")
            r = requests.get(f"{BASE_URL}/products/", headers={
                "Authorization": f"Bearer {token}"
            })
            print(f"Products Status: {r.status_code}")
            print(f"Products found: {len(r.json())}")
        else:
            print("Login Failed")

    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_api()
