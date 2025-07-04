from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from collections import deque
from copy import deepcopy
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# Comprehensive category and subcategory structure
categories = {
    'Electronics': {
        'Mobiles & Tablets': ['Smartphones', 'Tablets', 'Mobile Accessories'],
        'Computers & Laptops': ['Laptops', 'Desktops', 'Keyboards & Mice', 'Monitors'],
        'Audio & Video': ['Headphones', 'Bluetooth Speakers', 'Home Theaters']
    },
    'Fashion': {
        'Men': ['T-Shirts', 'Shirts', 'Jeans', 'Shoes'],
        'Women': ['Tops', 'Dresses', 'Sarees', 'Heels & Flats'],
        'Kids': ['Boys Clothing', 'Girls Clothing', 'Kids Footwear']
    },
    'Home & Kitchen': {
        'Furniture': ['Sofas', 'Beds', 'Chairs'],
        'Kitchen Appliances': ['Microwaves', 'Mixers & Grinders', 'Gas Stoves'],
        'Home Decor': ['Clocks', 'Paintings', 'Lighting']
    },
    'Grocery': {
        'Fruits & Vegetables': ['Fresh Fruits', 'Fresh Vegetables', 'Organic Produce'],
        'Dairy & Bakery': ['Milk & Dairy', 'Bread & Bakery', 'Eggs & Meat'],
        'Snacks & Beverages': ['Packaged Snacks', 'Beverages', 'Energy Drinks'],
        'Staples': ['Rice & Grains', 'Atta & Flours', 'Pulses & Lentils']
    },
    'Beauty & Personal Care': {
        'Skincare': ['Face Care', 'Body Care', 'Sunscreen'],
        'Haircare': ['Shampoo', 'Conditioner', 'Hair Styling'],
        'Fragrances': ['Men\'s Perfumes', 'Women\'s Perfumes', 'Deodorants'],
        'Makeup': ['Face Makeup', 'Eye Makeup', 'Lip Makeup']
    },
    'Toys, Baby & Kids': {
        'Baby Clothing': ['Baby Dresses', 'Baby Rompers', 'Baby Accessories'],
        'Diapers': ['Baby Diapers', 'Adult Diapers', 'Wipes'],
        'Toys & Games': ['Educational Toys', 'Outdoor Toys', 'Board Games'],
        'School Supplies': ['Stationery', 'School Bags', 'Art Supplies']
    },
    'Automotive': {
        'Car Accessories': ['Car Covers', 'Car Audio', 'Car Care'],
        'Bike Accessories': ['Helmets', 'Bike Covers', 'Bike Care'],
        'Oils & Lubricants': ['Engine Oil', 'Brake Oil', 'Coolant'],
        'Cleaning Supplies': ['Car Wash', 'Interior Cleaners', 'Polishes']
    }
}

# Sample product data with rupee prices
products = [
    # Electronics - Mobiles & Tablets
    {
        'id': 1,
        'name': 'iPhone 15 Pro',
        'brand': 'Apple',
        'price': 129999,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system.',
        'specs': {
            'RAM': '8GB',
            'Storage': '256GB',
            'Processor': 'A17 Pro',
            'Display': '6.1-inch OLED',
            'Battery': '3274mAh',
            'Camera': '48MP Triple',
            'OS': 'iOS 17'
        },
        'rating': 4.8,
        'reviews': 128,
        'badge': 'New',
        'in_stock': True
    },
    {
        'id': 2,
        'name': 'Samsung Galaxy S24',
        'brand': 'Samsung',
        'price': 99999,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'description': 'Flagship Samsung smartphone with AMOLED display and pro-grade camera.',
        'specs': {
            'RAM': '12GB',
            'Storage': '512GB',
            'Processor': 'Exynos 2400',
            'Display': '6.5-inch AMOLED',
            'Battery': '4000mAh',
            'Camera': '50MP Triple',
            'OS': 'Android 14'
        },
        'rating': 4.7,
        'reviews': 110,
        'badge': 'Popular',
        'in_stock': True
    },
    {
        'id': 3,
        'name': 'Redmi Note 13',
        'price': 18999,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'description': 'Affordable smartphone with long battery life and fast charging.',
        'rating': 4.5,
        'reviews': 90,
        'badge': 'Best Seller',
        'in_stock': True
    },
    {
        'id': 4,
        'name': 'Apple iPad Air',
        'price': 59999,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Tablets',
        'image': 'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'description': 'Lightweight tablet with Retina display and Apple Pencil support.',
        'rating': 4.6,
        'reviews': 70,
        'badge': 'Trending',
        'in_stock': True
    },
    {
        'id': 5,
        'name': 'Samsung Galaxy Tab S9',
        'price': 89999,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Tablets',
        'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Premium Android tablet with S Pen, perfect for productivity and entertainment.',
        'rating': 4.6,
        'reviews': 89,
        'badge': 'Hot',
        'in_stock': True
    },
    {
        'id': 6,
        'name': 'Apple AirPods Pro',
        'price': 24999,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Mobile Accessories',
        'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Wireless earbuds with active noise cancellation and spatial audio.',
        'rating': 4.7,
        'reviews': 256,
        'badge': 'Popular',
        'in_stock': True
    },
    {
        'id': 7,
        'name': 'Boat BassHeads 100',
        'price': 499,
        'category': 'Electronics',
        'subcategory': 'Mobiles & Tablets',
        'sub_subcategory': 'Mobile Accessories',
        'image': 'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'description': 'Affordable wired earphones with deep bass and clear sound.',
        'rating': 4.2,
        'reviews': 300,
        'badge': 'Budget',
        'in_stock': True
    },
    
    # Electronics - Computers & Laptops
    {
        'id': 8,
        'name': 'MacBook Pro 16"',
        'price': 249999,
        'category': 'Electronics',
        'subcategory': 'Computers & Laptops',
        'sub_subcategory': 'Laptops',
        'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?ixlib=rb-4.0.3&auto=format&fit=crop&w=2026&q=80',
        'description': 'Professional laptop with M3 Pro chip, perfect for creative work and development.',
        'rating': 4.9,
        'reviews': 203,
        'badge': 'Premium',
        'in_stock': True
    },
    {
        'id': 9,
        'name': 'Logitech MX Master 3S',
        'price': 8999,
        'category': 'Electronics',
        'subcategory': 'Computers & Laptops',
        'sub_subcategory': 'Keyboards & Mice',
        'image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Premium wireless mouse with ultra-quiet clicks and precision scrolling.',
        'rating': 4.5,
        'reviews': 156,
        'badge': 'Best Seller',
        'in_stock': True
    },
    
    # Electronics - Audio & Video
    {
        'id': 10,
        'name': 'Sony WH-1000XM5',
        'price': 34999,
        'category': 'Electronics',
        'subcategory': 'Audio & Video',
        'sub_subcategory': 'Headphones',
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Industry-leading noise-canceling headphones with exceptional sound quality.',
        'rating': 4.8,
        'reviews': 189,
        'badge': 'Top Rated',
        'in_stock': True
    },
    
    # Fashion - Men
    {
        'id': 11,
        'name': "Men's Cotton T-Shirt",
        'brand': 'Levis',
        'price': 899,
        'category': 'Fashion',
        'subcategory': 'Men',
        'sub_subcategory': 'T-Shirts',
        'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2080&q=80',
        'description': 'Comfortable cotton t-shirt with modern fit and breathable fabric.',
        'specs': {
            'Size': 'M',
            'Color': 'Blue',
            'Material': '100% Cotton',
            'Style': 'Regular Fit',
            'Sleeve': 'Short Sleeve'
        },
        'rating': 4.3,
        'reviews': 234,
        'badge': 'Trending',
        'in_stock': True
    },
    {
        'id': 12,
        'name': "Men's Formal Shirt",
        'brand': 'Arrow',
        'price': 1499,
        'category': 'Fashion',
        'subcategory': 'Men',
        'sub_subcategory': 'Shirts',
        'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2076&q=80',
        'description': 'Professional formal shirt perfect for office and special occasions.',
        'specs': {
            'Size': 'L',
            'Color': 'White',
            'Material': 'Cotton Blend',
            'Style': 'Slim Fit',
            'Sleeve': 'Long Sleeve'
        },
        'rating': 4.4,
        'reviews': 167,
        'badge': 'Classic',
        'in_stock': True
    },
    
    # Fashion - Women
    {
        'id': 13,
        'name': 'Women\'s Summer Dress',
        'price': 2499,
        'category': 'Fashion',
        'subcategory': 'Women',
        'sub_subcategory': 'Dresses',
        'image': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?ixlib=rb-4.0.3&auto=format&fit=crop&w=2076&q=80',
        'description': 'Elegant summer dress with floral pattern and comfortable fit.',
        'rating': 4.6,
        'reviews': 145,
        'badge': 'Summer Collection',
        'in_stock': True
    },
    {
        'id': 14,
        'name': 'Designer Saree',
        'price': 8999,
        'category': 'Fashion',
        'subcategory': 'Women',
        'sub_subcategory': 'Sarees',
        'image': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?ixlib=rb-4.0.3&auto=format&fit=crop&w=2076&q=80',
        'description': 'Traditional silk saree with intricate embroidery and elegant design.',
        'rating': 4.7,
        'reviews': 89,
        'badge': 'Traditional',
        'in_stock': False
    },
    
    # Home & Kitchen - Furniture
    {
        'id': 15,
        'name': 'Modern Sofa Set',
        'price': 45999,
        'category': 'Home & Kitchen',
        'subcategory': 'Furniture',
        'sub_subcategory': 'Sofas',
        'image': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
        'description': 'Contemporary 3-seater sofa with premium fabric and comfortable cushions.',
        'rating': 4.5,
        'reviews': 78,
        'badge': 'Premium',
        'in_stock': True
    },
    {
        'id': 16,
        'name': 'Queen Size Bed',
        'price': 29999,
        'category': 'Home & Kitchen',
        'subcategory': 'Furniture',
        'sub_subcategory': 'Beds',
        'image': 'https://images.unsplash.com/photo-1505693314120-0d443867891c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Elegant queen size bed with wooden frame and comfortable mattress.',
        'rating': 4.4,
        'reviews': 112,
        'badge': 'Best Value',
        'in_stock': True
    },
    
    # Home & Kitchen - Kitchen Appliances
    {
        'id': 17,
        'name': 'Samsung Microwave',
        'price': 8999,
        'category': 'Home & Kitchen',
        'subcategory': 'Kitchen Appliances',
        'sub_subcategory': 'Microwaves',
        'image': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': '25L convection microwave with smart cooking features and easy controls.',
        'rating': 4.3,
        'reviews': 156,
        'badge': 'Smart',
        'in_stock': True
    },
    
    # Grocery - Fruits & Vegetables
    {
        'id': 18,
        'name': 'Fresh Apple Pack',
        'price': 299,
        'category': 'Grocery',
        'subcategory': 'Fruits & Vegetables',
        'sub_subcategory': 'Fresh Fruits',
        'image': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
        'description': 'Fresh organic apples, 1kg pack with premium quality and sweet taste.',
        'rating': 4.6,
        'reviews': 445,
        'badge': 'Organic',
        'in_stock': True
    },
    {
        'id': 19,
        'name': 'Fresh Tomatoes',
        'price': 89,
        'category': 'Grocery',
        'subcategory': 'Fruits & Vegetables',
        'sub_subcategory': 'Fresh Vegetables',
        'image': 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Fresh red tomatoes, 500g pack perfect for cooking and salads.',
        'rating': 4.4,
        'reviews': 567,
        'badge': 'Fresh',
        'in_stock': True
    },
    
    # Beauty & Personal Care - Skincare
    {
        'id': 20,
        'name': 'Neutrogena Face Wash',
        'price': 599,
        'category': 'Beauty & Personal Care',
        'subcategory': 'Skincare',
        'sub_subcategory': 'Face Care',
        'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Gentle face wash for all skin types with deep cleansing formula.',
        'rating': 4.5,
        'reviews': 234,
        'badge': 'Dermatologist Recommended',
        'in_stock': True
    },
    
    # Toys, Baby & Kids - Toys & Games
    {
        'id': 21,
        'name': 'Educational Building Blocks',
        'price': 1499,
        'category': 'Toys, Baby & Kids',
        'subcategory': 'Toys & Games',
        'sub_subcategory': 'Educational Toys',
        'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'Colorful building blocks that enhance creativity and motor skills.',
        'rating': 4.7,
        'reviews': 189,
        'badge': 'Educational',
        'in_stock': True
    },
    
    # Automotive - Car Accessories
    {
        'id': 22,
        'name': 'Car Dashboard Camera',
        'price': 3999,
        'category': 'Automotive',
        'subcategory': 'Car Accessories',
        'sub_subcategory': 'Car Audio',
        'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        'description': 'HD dash cam with night vision and loop recording for safety.',
        'rating': 4.4,
        'reviews': 123,
        'badge': 'Safety',
        'in_stock': True
    }
]

@app.route('/')
def home():
    return render_template('index.html', categories=categories)

@app.route('/products')
def products_page():
    category = request.args.get('category', '')
    subcategory = request.args.get('subcategory', '')
    sub_subcategory = request.args.get('sub_subcategory', '')
    search = request.args.get('search', '')
    brand = request.args.get('brand', '')
    # For technical filters, get all possible keys from specs
    spec_filters = {k: request.args.get(k, '') for k in ['RAM', 'Storage', 'Processor', 'Display', 'Battery', 'Camera', 'OS', 'Size', 'Color', 'Material', 'Style', 'Sleeve']}

    filtered_products = products

    if category:
        filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
    if subcategory:
        filtered_products = [p for p in filtered_products if p['subcategory'].lower() == subcategory.lower()]
    if sub_subcategory:
        filtered_products = [p for p in filtered_products if p['sub_subcategory'].lower() == sub_subcategory.lower()]
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower() or search.lower() in p['description'].lower()]
    if brand:
        filtered_products = [p for p in filtered_products if p.get('brand', '').lower() == brand.lower()]
    for k, v in spec_filters.items():
        if v:
            filtered_products = [p for p in filtered_products if p.get('specs', {}).get(k, '').lower() == v.lower()]

    # Extract available brands and specs for current filter context
    available_brands = sorted(set(p.get('brand') for p in filtered_products if p.get('brand')))
    available_specs = {}
    for p in filtered_products:
        for k, v in p.get('specs', {}).items():
            if k not in available_specs:
                available_specs[k] = set()
            available_specs[k].add(v)
    for k in available_specs:
        available_specs[k] = sorted(available_specs[k])

    return render_template('products.html',
        products=filtered_products,
        categories=categories,
        current_category=category,
        current_subcategory=subcategory,
        current_sub_subcategory=sub_subcategory,
        search=search,
        available_brands=available_brands,
        available_specs=available_specs,
        selected_brand=brand,
        selected_specs=spec_filters
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    
    # Track viewed products in session
    viewed = deque(session.get('viewed_products', []), maxlen=10)
    if product_id not in viewed:
        viewed.append(product_id)
    session['viewed_products'] = list(viewed)
    
    # Get related products from same category
    related_products = [p for p in products if p['category'] == product['category'] and p['id'] != product_id][:3]
    
    # Get also viewed products (excluding current)
    also_viewed_products = [p for p in products if p['id'] in viewed and p['id'] != product_id]
    
    return render_template('product_detail.html', product=product, related_products=related_products, also_viewed_products=also_viewed_products)

@app.route('/categories')
def categories_page():
    return render_template('categories.html', categories=categories)

@app.route('/api/products')
def api_products():
    category = request.args.get('category', '')
    subcategory = request.args.get('subcategory', '')
    sub_subcategory = request.args.get('sub_subcategory', '')
    search = request.args.get('search', '')
    
    filtered_products = products
    
    if category:
        filtered_products = [p for p in products if p['category'].lower() == category.lower()]
    
    if subcategory:
        filtered_products = [p for p in filtered_products if p['subcategory'].lower() == subcategory.lower()]
    
    if sub_subcategory:
        filtered_products = [p for p in filtered_products if p['sub_subcategory'].lower() == sub_subcategory.lower()]
    
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower()]
    
    return jsonify(filtered_products)

@app.route('/api/product/<int:product_id>')
def api_product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product)

@app.route('/api/categories')
def api_categories():
    return jsonify(categories)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    cart = session.get('cart', [])
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['qty'] += 1
            found = True
            break
    if not found:
        cart.append({'id': product_id, 'qty': 1})
    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': sum(item['qty'] for item in cart)})

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': sum(item['qty'] for item in cart)})

@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    qty = int(request.form.get('qty', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['qty'] = max(1, qty)
            break
    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': sum(item['qty'] for item in cart)})

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    wishlist = session.get('wishlist', [])
    if product_id not in wishlist:
        wishlist.append(product_id)
    session['wishlist'] = wishlist
    return jsonify({'success': True, 'wishlist_count': len(wishlist)})

@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
def remove_from_wishlist(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    wishlist = session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    session['wishlist'] = wishlist
    return jsonify({'success': True, 'wishlist_count': len(wishlist)})

@app.route('/move_to_cart/<int:product_id>', methods=['POST'])
def move_to_cart(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    wishlist = session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    session['wishlist'] = wishlist
    # Add to cart (qty=1 or increment if exists)
    cart = session.get('cart', [])
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['qty'] += 1
            found = True
            break
    if not found:
        cart.append({'id': product_id, 'qty': 1})
    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': sum(item['qty'] for item in cart), 'wishlist_count': len(wishlist)})

@app.route('/move_to_wishlist/<int:product_id>', methods=['POST'])
def move_to_wishlist(product_id):
    if not session.get('user_logged_in'):
        return jsonify({'login_required': True}), 401
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    wishlist = session.get('wishlist', [])
    if product_id not in wishlist:
        wishlist.append(product_id)
    session['wishlist'] = wishlist
    return jsonify({'success': True, 'cart_count': sum(item['qty'] for item in cart), 'wishlist_count': len(wishlist)})

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    cart_products = []
    for item in cart:
        product = next((p for p in products if p['id'] == item['id']), None)
        if product:
            prod_copy = product.copy()
            prod_copy['qty'] = item['qty']
            cart_products.append(prod_copy)
    return render_template('cart.html', products=cart_products)

@app.route('/wishlist')
def view_wishlist():
    wishlist = session.get('wishlist', [])
    wishlist_products = [p for p in products if p['id'] in wishlist]
    return render_template('wishlist.html', products=wishlist_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        # Simple validation - in a real app, you'd check against a database
        if email == 'demo@example.com' and password == 'password123':
            session['user_logged_in'] = True
            session['user_email'] = email
            session['user_name'] = 'Demo User'
            if remember:
                session.permanent = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')
        
        # Validation
        if not all([first_name, last_name, email, phone, password, confirm_password]):
            return render_template('register.html', error='All fields are required')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if password and len(password) < 8:
            return render_template('register.html', error='Password must be at least 8 characters long')
        
        if not terms:
            return render_template('register.html', error='You must agree to the terms and conditions')
        
        # In a real app, you'd save to database and hash the password
        # For demo purposes, we'll just log them in
        session['user_logged_in'] = True
        session['user_email'] = email
        session['user_name'] = f'{first_name} {last_name}'
        
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    user_info = {
        'name': session.get('user_name', ''),
        'email': session.get('user_email', ''),
        'phone': session.get('user_phone', ''),
    }
    addresses = session.get('addresses', [])
    orders = session.get('orders', [])
    return render_template('profile.html', user=user_info, addresses=addresses, orders=orders)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        if not all([name, email, phone]):
            return render_template('edit_profile.html', error='All fields are required', user={
                'name': name,
                'email': email,
                'phone': phone
            })
        session['user_name'] = name
        session['user_email'] = email
        session['user_phone'] = phone
        return redirect(url_for('profile'))
    user_info = {
        'name': session.get('user_name', ''),
        'email': session.get('user_email', ''),
        'phone': session.get('user_phone', ''),
    }
    return render_template('edit_profile.html', user=user_info)

@app.route('/addresses')
def addresses():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    addresses = session.get('addresses', [])
    return render_template('addresses.html', addresses=addresses)

@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        address = {
            'id': len(session.get('addresses', [])) + 1,
            'name': request.form.get('name'),
            'line1': request.form.get('line1'),
            'line2': request.form.get('line2'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'zip': request.form.get('zip'),
            'phone': request.form.get('phone'),
        }
        if not all([address['name'], address['line1'], address['city'], address['state'], address['zip'], address['phone']]):
            return render_template('add_address.html', error='All required fields must be filled', address=address)
        addresses = session.get('addresses', [])
        addresses.append(address)
        session['addresses'] = addresses
        return redirect(url_for('profile'))
    return render_template('add_address.html')

@app.route('/edit_address/<int:address_id>', methods=['GET', 'POST'])
def edit_address(address_id):
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    addresses = session.get('addresses', [])
    address = next((a for a in addresses if a['id'] == address_id), None)
    if not address:
        return 'Address not found', 404
    if request.method == 'POST':
        address['name'] = request.form.get('name')
        address['line1'] = request.form.get('line1')
        address['line2'] = request.form.get('line2')
        address['city'] = request.form.get('city')
        address['state'] = request.form.get('state')
        address['zip'] = request.form.get('zip')
        address['phone'] = request.form.get('phone')
        if not all([address['name'], address['line1'], address['city'], address['state'], address['zip'], address['phone']]):
            return render_template('edit_address.html', error='All required fields must be filled', address=address)
        # Save back
        for i, a in enumerate(addresses):
            if a['id'] == address_id:
                addresses[i] = address
        session['addresses'] = addresses
        return redirect(url_for('profile'))
    return render_template('edit_address.html', address=address)

@app.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    addresses = session.get('addresses', [])
    addresses = [a for a in addresses if a['id'] != address_id]
    session['addresses'] = addresses
    return redirect(url_for('profile'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('cart'))
    addresses = session.get('addresses', [])
    selected_address_id = request.form.get('address_id') if request.method == 'POST' else None
    selected_address = None
    if selected_address_id:
        selected_address = next((a for a in addresses if str(a['id']) == str(selected_address_id)), None)
    if request.method == 'POST':
        # Add address if needed
        if request.form.get('add_address'):
            address = {
                'id': len(addresses) + 1,
                'name': request.form.get('name'),
                'line1': request.form.get('line1'),
                'line2': request.form.get('line2'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'zip': request.form.get('zip'),
                'phone': request.form.get('phone'),
            }
            if not all([address['name'], address['line1'], address['city'], address['state'], address['zip'], address['phone']]):
                return render_template('checkout.html', error='All required fields must be filled', addresses=addresses, cart=cart, products=get_cart_products(cart), selected_address=None)
            addresses.append(address)
            session['addresses'] = addresses
            selected_address = address
        # Place order
        if selected_address or request.form.get('add_address'):
            order_id = str(uuid4())[:8]
            order = {
                'id': order_id,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'items': get_cart_products(cart),
                'total': sum(p['price'] * p['qty'] for p in get_cart_products(cart)),
                'address': selected_address,
                'status': 'Confirmed',
            }
            orders = session.get('orders', [])
            orders.append(order)
            session['orders'] = orders
            session['cart'] = []  # Clear cart
            return redirect(url_for('order_success', order_id=order_id))
    return render_template('checkout.html', addresses=addresses, cart=cart, products=get_cart_products(cart), selected_address=selected_address)

def get_cart_products(cart):
    cart_products = []
    for item in cart:
        product = next((p for p in products if p['id'] == item['id']), None)
        if product:
            prod_copy = product.copy()
            prod_copy['qty'] = item['qty']
            cart_products.append(prod_copy)
    return cart_products

@app.route('/order/<order_id>')
def order_success(order_id):
    orders = session.get('orders', [])
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return 'Order not found', 404
    return render_template('order_success.html', order=order)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'admin@example.com' and password == 'admin123':
            session['admin_logged_in'] = True
            session['admin_email'] = email
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/products')
def admin_products():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    search = request.args.get('search', '').strip().lower()
    filtered_products = products
    if search:
        filtered_products = [p for p in products if search in p['name'].lower() or search in p.get('brand', '').lower()]
    return render_template('admin_products.html', products=filtered_products, search=search)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        new_id = max(p['id'] for p in products) + 1 if products else 1
        product = {
            'id': new_id,
            'name': request.form.get('name'),
            'brand': request.form.get('brand'),
            'price': int(request.form.get('price', 0)),
            'category': request.form.get('category'),
            'subcategory': request.form.get('subcategory'),
            'sub_subcategory': request.form.get('sub_subcategory'),
            'image': request.form.get('image'),
            'description': request.form.get('description'),
            'specs': {},
            'rating': float(request.form.get('rating', 0)),
            'reviews': int(request.form.get('reviews', 0)),
            'badge': request.form.get('badge'),
            'in_stock': request.form.get('in_stock') == 'on',
        }
        # Parse specs
        for key in ['RAM', 'Storage', 'Processor', 'Display', 'Battery', 'Camera', 'OS', 'Size', 'Color', 'Material', 'Style', 'Sleeve']:
            val = request.form.get(key)
            if val:
                product['specs'][key] = val
        products.append(product)
        return redirect(url_for('admin_products'))
    return render_template('admin_edit_product.html', product=None, categories=categories)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return 'Product not found', 404
    if request.method == 'POST':
        product['name'] = request.form.get('name')
        product['brand'] = request.form.get('brand')
        product['price'] = int(request.form.get('price', 0))
        product['category'] = request.form.get('category')
        product['subcategory'] = request.form.get('subcategory')
        product['sub_subcategory'] = request.form.get('sub_subcategory')
        product['image'] = request.form.get('image')
        product['description'] = request.form.get('description')
        product['rating'] = float(request.form.get('rating', 0))
        product['reviews'] = int(request.form.get('reviews', 0))
        product['badge'] = request.form.get('badge')
        product['in_stock'] = request.form.get('in_stock') == 'on'
        # Parse specs
        product['specs'] = {}
        for key in ['RAM', 'Storage', 'Processor', 'Display', 'Battery', 'Camera', 'OS', 'Size', 'Color', 'Material', 'Style', 'Sleeve']:
            val = request.form.get(key)
            if val:
                product['specs'][key] = val
        return redirect(url_for('admin_products'))
    return render_template('admin_edit_product.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def admin_delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    global products
    products = [p for p in products if p['id'] != product_id]
    return redirect(url_for('admin_products'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 