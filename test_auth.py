"""
Script de prueba para endpoints de autenticación.
Uso: python test_auth.py [URL]

Ejemplo:
  python test_auth.py http://localhost:8000
  python test_auth.py https://web-production-f69ce.up.railway.app
"""
import sys
import requests
import json
from datetime import datetime

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_success(message):
    print(f"{GREEN}✓{RESET} {message}")


def print_error(message):
    print(f"{RED}✗{RESET} {message}")


def print_info(message):
    print(f"{BLUE}ℹ{RESET} {message}")


def print_warning(message):
    print(f"{YELLOW}⚠{RESET} {message}")


def test_healthcheck(base_url):
    """Test healthcheck endpoint."""
    print("\n" + "="*60)
    print("TEST 1: Healthcheck")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/healthz", timeout=10)
        
        if response.status_code == 200:
            print_success(f"Healthcheck OK: {response.json()}")
            return True
        else:
            print_error(f"Healthcheck failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Healthcheck error: {e}")
        return False


def test_register(base_url):
    """Test user registration."""
    print("\n" + "="*60)
    print("TEST 2: User Registration")
    print("="*60)
    
    # Generate unique email
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    email = f"test_{timestamp}@example.com"
    
    user_data = {
        "email": email,
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    print_info(f"Registering user: {email}")
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 201:
            user = response.json()
            print_success("User registered successfully!")
            print(f"  ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user['full_name']}")
            print(f"  Active: {user['is_active']}")
            print(f"  Verified: {user['is_verified']}")
            return email, user_data["password"]
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None, None
    except Exception as e:
        print_error(f"Registration error: {e}")
        return None, None


def test_login(base_url, email, password):
    """Test user login."""
    print("\n" + "="*60)
    print("TEST 3: User Login")
    print("="*60)
    
    if not email or not password:
        print_warning("Skipping login test (no user registered)")
        return None
    
    print_info(f"Logging in as: {email}")
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            data={
                "username": email,
                "password": password
            },
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print_success("Login successful!")
            print(f"  Token type: {token_data['token_type']}")
            print(f"  Token (first 50 chars): {token[:50]}...")
            return token
        else:
            print_error(f"Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None


def test_get_me(base_url, token):
    """Test get current user endpoint."""
    print("\n" + "="*60)
    print("TEST 4: Get Current User")
    print("="*60)
    
    if not token:
        print_warning("Skipping get_me test (no token)")
        return False
    
    print_info("Getting current user info...")
    
    try:
        response = requests.get(
            f"{base_url}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            user = response.json()
            print_success("User info retrieved successfully!")
            print(f"  ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user['full_name']}")
            print(f"  Active: {user['is_active']}")
            print(f"  Verified: {user['is_verified']}")
            return True
        else:
            print_error(f"Get user failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Get user error: {e}")
        return False


def test_invalid_token(base_url):
    """Test with invalid token."""
    print("\n" + "="*60)
    print("TEST 5: Invalid Token (should fail)")
    print("="*60)
    
    print_info("Testing with invalid token...")
    
    try:
        response = requests.get(
            f"{base_url}/api/auth/me",
            headers={"Authorization": "Bearer invalid_token_12345"},
            timeout=10
        )
        
        if response.status_code == 401:
            print_success("Invalid token correctly rejected!")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Invalid token test error: {e}")
        return False


def main():
    """Run all tests."""
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = "http://localhost:8000"
    
    print("\n" + "="*60)
    print(f"🧪 TESTING AUTHENTICATION SYSTEM")
    print(f"📍 Base URL: {base_url}")
    print("="*60)
    
    # Run tests
    results = []
    
    # Test 1: Healthcheck
    results.append(("Healthcheck", test_healthcheck(base_url)))
    
    # Test 2: Register
    email, password = test_register(base_url)
    results.append(("Registration", email is not None))
    
    # Test 3: Login
    token = test_login(base_url, email, password)
    results.append(("Login", token is not None))
    
    # Test 4: Get current user
    results.append(("Get Current User", test_get_me(base_url, token)))
    
    # Test 5: Invalid token
    results.append(("Invalid Token", test_invalid_token(base_url)))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name}: {status}")
    
    print("\n" + "-"*60)
    print(f"  Total: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print(f"\n{GREEN}🎉 ALL TESTS PASSED!{RESET}")
        print(f"\n{BLUE}✓ Your authentication system is working correctly!{RESET}")
        return 0
    else:
        print(f"\n{RED}❌ SOME TESTS FAILED{RESET}")
        print(f"\n{YELLOW}Check the errors above and verify:{RESET}")
        print("  1. Database is configured correctly")
        print("  2. All environment variables are set")
        print("  3. Tables are created in PostgreSQL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
