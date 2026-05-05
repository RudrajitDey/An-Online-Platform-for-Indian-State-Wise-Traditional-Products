# An Online Platform for Indian State-Wise Traditional Products

A comprehensive e-commerce platform dedicated to showcasing and selling traditional Indian products organized by states. This platform connects local artisans and vendors with customers nationwide, preserving India's rich cultural heritage.

## 🌟 Features

### **For Customers**
- **State-wise Product Browsing**: Explore traditional products from different Indian states
- **Advanced Search**: Search products by name, category, or state
- **Product Details**: Detailed product information with images, descriptions, and vendor details
- **Shopping Cart**: Add to cart, manage quantities, view stock availability
- **Secure Checkout**: Multi-step checkout process with address management
- **Payment Integration**: PayPal integration and Cash on Delivery options
- **Order Tracking**: View order history and track order status
- **User Account**: Personal dashboard with order management

### **For Vendors**
- **Product Management**: Add, edit, and manage product listings
- **Inventory Management**: Track product stock and availability
- **Order Processing**: View and manage customer orders
- **Vendor Dashboard**: Comprehensive dashboard for business insights

### **For Administrators**
- **Admin Dashboard**: Complete oversight of platform operations
- **User Management**: Manage customers and vendors
- **Seller Verification**: Approve and manage vendor registrations
- **Order Management**: Monitor and manage all platform orders

## 🛠️ Technology Stack

### **Backend**
- **Framework**: Django 4.x
- **Language**: Python 3.8+
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django's built-in authentication system

### **Frontend**
- **Templates**: Django Templates with HTML5
- **Styling**: CSS3 with responsive design
- **JavaScript**: Vanilla JavaScript for interactive features
- **Payment**: PayPal JavaScript SDK

### **Development Tools**
- **Version Control**: Git
- **Package Management**: pip
- **Static Files**: Django's static file management

## 📁 Project Structure

```
Indian_Traditional_Shop/
├── Home/                    # Core product and category management
│   ├── models.py           # Product, Category, State models
│   ├── views.py            # Home, product listing, search
│   └── templates/          # Product display templates
├── accounts/               # User authentication and profiles
│   ├── models.py           # User profile models
│   ├── views.py            # Login, register, dashboard
│   └── templates/          # Authentication templates
├── cart/                   # Shopping cart functionality
│   ├── models.py           # Cart and CartItem models
│   ├── views.py            # Cart operations, checkout
│   └── templates/          # Cart and checkout templates
├── orders/                 # Order processing and payments
│   ├── models.py           # Order, Payment, OrderProduct models
│   ├── views.py            # Order processing, payment handling
│   └── templates/          # Payment and order confirmation
├── shop/                   # Additional shop functionality
├── static/                 # CSS, JavaScript, images
├── templates/              # Base templates and shared templates
└── media/                  # User uploaded content
```

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git

### **Installation Steps**

1. **Clone the repository**
   ```bash
   git clone https://github.com/RudrajitDey/An-Online-Platform-for-Indian-State-Wise-Traditional-Products.git
   cd Indian_Traditional_Shop
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Create requirements.txt with `pip freeze > requirements.txt`*

4. **Environment Setup**
   ```bash
   # Create .env file (optional)
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Database Migration**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application**
   - Main Site: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 🏪 Core Features Explained

### **Product Management**
- **State-wise Categorization**: Products organized by Indian states
- **Vendor System**: Each product associated with a vendor
- **Stock Management**: Real-time stock tracking and availability display
- **Product Details**: Rich product information with images and descriptions

### **Shopping Experience**
- **Cart Functionality**: Add/remove items, quantity adjustment
- **Stock Display**: Real-time stock availability in cart
- **Checkout Process**: Multi-step checkout with address validation
- **Payment Options**: PayPal integration and Cash on Delivery

### **Order Processing**
- **Order Creation**: Automatic order generation from cart
- **Payment Processing**: Secure payment handling with multiple options
- **Order Confirmation**: Email notifications and order tracking
- **Status Management**: Order status updates and tracking

### **User Management**
- **Customer Accounts**: Registration, login, profile management
- **Vendor Accounts**: Product management, order processing
- **Admin Dashboard**: Complete platform oversight

## 🎯 Key Models

### **Product Model**
- Name, description, price, stock
- Associated vendor and category
- State-wise classification
- Product images and metadata

### **Order Model**
- Order details, customer information
- Payment status and tracking
- Order status management
- Tax and total calculations

### **Cart Model**
- User-specific shopping carts
- Item quantity and pricing
- Stock validation
- Session management

## 🔧 Configuration

### **Settings Configuration**
```python
# Django Settings
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### **PayPal Integration**
```python
# PayPal Settings (add to settings.py)
PAYPAL_CLIENT_ID = 'your-paypal-client-id'
PAYPAL_SECRET = 'your-paypal-secret'
PAYPAL_MODE = 'sandbox'  # or 'live'
```

## 📱 Responsive Design

The platform features a fully responsive design that works seamlessly across:
- Desktop computers
- Tablets
- Mobile devices

### **Key Responsive Features**
- Mobile-friendly navigation
- Touch-optimized interface
- Adaptive layout for different screen sizes
- Optimized checkout flow for mobile

## 🔐 Security Features

- **CSRF Protection**: Django's built-in CSRF protection
- **Password Hashing**: Secure password storage
- **Session Management**: Secure session handling
- **Input Validation**: Form validation and sanitization
- **SQL Injection Prevention**: Django ORM protection

## 📊 Admin Features

### **Admin Dashboard Access**
- URL: `/admin/`
- Features: User management, product oversight, order monitoring

### **Vendor Management**
- Seller registration approval
- Product listing management
- Order processing capabilities

## 🚀 Deployment Considerations

### **Production Setup**
1. **Database**: Switch to PostgreSQL
2. **Static Files**: Configure CDN or static file server
3. **Environment Variables**: Use environment-specific settings
4. **Security**: Set DEBUG=False, configure ALLOWED_HOSTS
5. **Domain**: Configure domain and SSL certificate

### **Performance Optimization**
- Database indexing
- Image optimization
- Caching strategies
- CDN integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

**Project Maintainer**: Rudrajit Dey
**GitHub**: https://github.com/RudrajitDey
**Project URL**: https://github.com/RudrajitDey/An-Online-Platform-for-Indian-State-Wise-Traditional-Products

## 🙏 Acknowledgments

- Django Framework for robust backend development
- PayPal for payment processing integration
- All contributors and supporters of traditional Indian crafts
- Local artisans and vendors who make these products available

---

## 📈 Future Enhancements

- **Multi-language Support**: Support for regional Indian languages
- **Advanced Search**: AI-powered product recommendations
- **Mobile App**: Native mobile applications
- **Vendor Analytics**: Advanced analytics for vendors
- **Social Integration**: Social media sharing and login
- **Review System**: Customer reviews and ratings
- **Wishlist Feature**: Save products for later purchase
- **Discount System**: Coupon and discount management
- **Shipping Integration**: Real-time shipping calculation
- **Live Chat**: Customer support chat system

---

**Made with ❤️ for promoting Indian Traditional Products**
