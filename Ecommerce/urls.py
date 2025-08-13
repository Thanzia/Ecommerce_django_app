"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_app.views import *
from store.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', IndexView.as_view(), name='index'),
	
	path('user/signup/', UserRegistrationView.as_view(), name='signup'),
	path('user/otp_verify/', OtpVerificationView.as_view(), name='otp_verify'),
	path('user/login/', LoginView.as_view(), name='login'),
	path('user/login/email/', LoginEmailView.as_view(), name='login_email'),
	path('user/logout/', LogoutView.as_view(), name='logout'),
	path('user/forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
	path('user/reset_password/', ResetPasswordView.as_view(), name='reset_pwd'),
	path('user/verify_otp/', OtpVerifyView.as_view(), name='pwdotp_verify'),

    path('store/products/', ProductListView.as_view(), name='products_list'),
    path('store/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('store/add_to_cart/<int:pk>/', AddtoCartView.as_view(), name='add_to_cart'),
    path('store/cart_summary/', CartSummaryView.as_view(), name='cart_summary'),
    path('store/cart_summary/remove/<int:pk>/', CartSummaryRemove.as_view(), name='cart_summary_remove'),
    path('store/add_to_wishlist/<int:pk>/', AddWishlistItem.as_view(), name='add_to_wishlist'),
    path('store/wishlist/', WishlistView.as_view(), name='wishlist'),
    path('store/wishlist/remove/<int:pk>/', WishlistRemoveItem.as_view(), name='wishlist_remove'),

    path('store/order/', OrderView.as_view(), name='order'),
    path('store/payment_success/', PaymentSucessView.as_view(), name='payment_success'),
    path('order/summary/', OrderSummary.as_view(), name='order_summary'),


    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path('returns/', returns_view, name='returns'),
    path('privacy/', privacy_view, name='privacy'),
    path('careers/', careers_view, name='careers'),
	path('shipping/', shipping_view, name='shipping'),
	

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
