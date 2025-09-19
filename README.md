# 🛒 Ecommerce Django App

A full-stack Ecommerce platform built with Django and Django REST Framework.  
Features secure user authentication, product management, cart, wishlist, and checkout.

---

## 🚀 Features
- User registration and JWT authentication
- Product catalog with images
- Cart and wishlist management
- Checkout with payment integration (Razorpay/Stripe, if configured)
- Admin panel for managing products & orders
- Responsive frontend (React/Bootstrap/Tailwind)

---

## 📦 Tech Stack
- **Backend:** Django, Django REST Framework, JWT
- **Database:** SQLite / PostgreSQL
- **Auth:** Django auth + SimpleJWT
- **Other:** Pillow for image handling

---

## ⚙️ Setup Instructions

### 1. Clone Repository 
```bash
git clone https://github.com/<your-username>/EcommerceApp.git
cd EcommerceApp

### 2. Create Virtual Environment

python -m venv venv
# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure Environment Variables
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

### 5. Run Migrations
python manage.py migrate

### 6. Start Development server
python manage.py runserver
# App will run on http://127.0.0.1:8000/
