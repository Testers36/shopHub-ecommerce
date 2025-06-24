# 🛍️ ShopHub - Modern Ecommerce Website

A fully-featured ecommerce website built with Flask, featuring modern UI design, user authentication, shopping cart functionality, and comprehensive product management.

![ShopHub](https://img.shields.io/badge/Flask-2.3.3-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🛒 Shopping Experience
- **Product Catalog** - 22+ products across 7 categories
- **Advanced Filtering** - Filter by category, subcategory, brand, and technical specifications
- **Search Functionality** - Search products by name and description
- **Product Details** - Comprehensive product pages with specifications and ratings
- **"Also Viewed" Recommendations** - Session-based product suggestions

### 👤 User Management
- **User Authentication** - Login and registration system
- **Session Management** - Secure user sessions with remember me functionality
- **User Profiles** - Account management and order history
- **Demo Account** - Test with pre-configured credentials

### 🛍️ Shopping Features
- **Shopping Cart** - Add/remove items with quantity controls
- **Wishlist** - Save items for later purchase
- **Order Summary** - Calculate totals with tax and shipping
- **AJAX Integration** - Smooth user experience without page reloads

### 🎨 Modern UI/UX
- **Responsive Design** - Mobile-friendly layouts
- **Amazon-like Sidebar** - Category navigation
- **Modern Styling** - Professional design with gradients and animations
- **Interactive Elements** - Hover effects and smooth transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shopHub-ecommerce.git
   cd shopHub-ecommerce
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔐 Demo Credentials

For testing purposes, use these demo credentials:
- **Email**: `demo@example.com`
- **Password**: `password123`

## 📁 Project Structure

```
ecommerce-site/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
└── templates/            # HTML templates
    ├── index.html        # Homepage
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── products.html     # Product catalog
    ├── product_detail.html # Individual product page
    ├── cart.html         # Shopping cart
    ├── wishlist.html     # User wishlist
    ├── categories.html   # Category listing
    └── sidebar.html      # Navigation sidebar
```

## 🛍️ Product Categories

The website features 7 main categories with subcategories:

1. **Electronics**
   - Mobiles & Tablets (Smartphones, Tablets, Mobile Accessories)
   - Computers & Laptops (Laptops, Desktops, Keyboards & Mice, Monitors)
   - Audio & Video (Headphones, Bluetooth Speakers, Home Theaters)

2. **Fashion**
   - Men (T-Shirts, Shirts, Jeans, Shoes)
   - Women (Tops, Dresses, Sarees, Heels & Flats)
   - Kids (Boys Clothing, Girls Clothing, Kids Footwear)

3. **Home & Kitchen**
   - Furniture (Sofas, Beds, Chairs)
   - Kitchen Appliances (Microwaves, Mixers & Grinders, Gas Stoves)
   - Home Decor (Clocks, Paintings, Lighting)

4. **Grocery**
   - Fruits & Vegetables (Fresh Fruits, Fresh Vegetables, Organic Produce)
   - Dairy & Bakery (Milk & Dairy, Bread & Bakery, Eggs & Meat)
   - Snacks & Beverages (Packaged Snacks, Beverages, Energy Drinks)
   - Staples (Rice & Grains, Atta & Flours, Pulses & Lentils)

5. **Beauty & Personal Care**
   - Skincare (Face Care, Body Care, Sunscreen)
   - Haircare (Shampoo, Conditioner, Hair Styling)
   - Fragrances (Men's Perfumes, Women's Perfumes, Deodorants)
   - Makeup (Face Makeup, Eye Makeup, Lip Makeup)

6. **Toys, Baby & Kids**
   - Baby Clothing (Baby Dresses, Baby Rompers, Baby Accessories)
   - Diapers (Baby Diapers, Adult Diapers, Wipes)
   - Toys & Games (Educational Toys, Outdoor Toys, Board Games)
   - School Supplies (Stationery, School Bags, Art Supplies)

7. **Automotive**
   - Car Accessories (Car Covers, Car Audio, Car Care)
   - Bike Accessories (Helmets, Bike Covers, Bike Care)
   - Oils & Lubricants (Engine Oil, Brake Oil, Coolant)
   - Cleaning Supplies (Car Wash, Interior Cleaners, Polishes)

## 🔧 API Endpoints

The application provides RESTful API endpoints:

- `GET /api/products` - Get all products with optional filters
- `GET /api/product/<id>` - Get specific product details
- `GET /api/categories` - Get category structure
- `POST /add_to_cart/<id>` - Add product to cart
- `POST /add_to_wishlist/<id>` - Add product to wishlist
- `POST /remove_from_wishlist/<id>` - Remove product from wishlist

## 🎯 Key Features Explained

### Dynamic Filtering
Products can be filtered by:
- Category and subcategory
- Brand
- Technical specifications (RAM, Storage, Processor, etc.)
- Price range
- Availability

### Session Management
- Secure user sessions with Flask sessions
- Cart and wishlist persistence across browser sessions
- "Remember me" functionality for login

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Touch-friendly interface elements

## 🛠️ Customization

### Adding New Products
Edit the `products` list in `app.py` to add new products:

```python
{
    'id': 23,
    'name': 'Product Name',
    'brand': 'Brand Name',
    'price': 9999,
    'category': 'Electronics',
    'subcategory': 'Mobiles & Tablets',
    'sub_subcategory': 'Smartphones',
    'image': 'image_url',
    'description': 'Product description',
    'specs': {
        'RAM': '8GB',
        'Storage': '256GB'
    },
    'rating': 4.5,
    'reviews': 100,
    'badge': 'New',
    'in_stock': True
}
```

### Styling Customization
- Modify CSS in the HTML templates
- Update color schemes in the style sections
- Customize animations and transitions

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using environment variables for configuration
- Implementing proper database integration
- Adding SSL/TLS certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework and community
- Font Awesome for icons
- Unsplash for product images
- Modern CSS techniques and best practices

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation
- Review the code comments

---

**Happy Shopping! 🛍️** 