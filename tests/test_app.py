import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"ShopHub" in response.data

def test_products_page(client):
    response = client.get('/products')
    assert response.status_code == 200

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login_success(client):
    response = client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"ShopHub" in response.data

def test_login_failure(client):
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    })
    assert b"Invalid email or password" in response.data

def test_add_to_cart_requires_login(client):
    response = client.post('/add_to_cart/1')
    assert response.status_code == 401
    assert b'login_required' in response.data

def test_add_to_cart_after_login(client):
    # Login first
    client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'password123'
    })
    # Add to cart
    response = client.post('/add_to_cart/1')
    assert response.status_code == 200
    assert b'success' in response.data
    # Check cart page
    response = client.get('/cart')
    assert response.status_code == 200
    assert b'iPhone' in response.data or b'cart' in response.data

def test_add_to_wishlist_requires_login(client):
    response = client.post('/add_to_wishlist/1')
    assert response.status_code == 401
    assert b'login_required' in response.data

def test_add_to_wishlist_after_login(client):
    client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'password123'
    })
    response = client.post('/add_to_wishlist/1')
    assert response.status_code == 200
    assert b'success' in response.data
    # Remove from wishlist
    response = client.post('/remove_from_wishlist/1')
    assert response.status_code == 200
    assert b'success' in response.data

def test_checkout_requires_login(client):
    response = client.get('/checkout')
    # Should redirect to login
    assert response.status_code in (301, 302)

def test_checkout_flow(client):
    # Login
    client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'password123'
    })
    # Add to cart
    client.post('/add_to_cart/1')
    # Add address
    address_data = {
        'name': 'Test User',
        'line1': '123 Test St',
        'line2': '',
        'city': 'Testville',
        'state': 'TS',
        'zip': '12345',
        'phone': '1234567890',
        'add_address': '1'
    }
    response = client.post('/checkout', data=address_data, follow_redirects=True)
    assert b'Order' in response.data or b'Success' in response.data

def test_admin_login_success(client):
    response = client.post('/admin/login', data={
        'email': 'admin@example.com',
        'password': 'admin123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'admin' in response.data

def test_admin_login_failure(client):
    response = client.post('/admin/login', data={
        'email': 'wrong@admin.com',
        'password': 'wrongpass'
    })
    assert b'Invalid credentials' in response.data

def test_admin_products_requires_login(client):
    response = client.get('/admin/products')
    # Should redirect to admin login
    assert response.status_code in (301, 302)

def test_admin_products_after_login(client):
    client.post('/admin/login', data={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    response = client.get('/admin/products')
    assert response.status_code == 200
    assert b'Product' in response.data or b'Add Product' in response.data 