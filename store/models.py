from django.db import models
from user_app.models import *


# Create your models here.

# category model
class CategoryModel(models.Model):

	name = models.CharField(max_length=100)

	def __str__(self):

		return self.name
	

# product model
class Product(models.Model):

	name = models.CharField(max_length=255)

	description = models.TextField()

	price = models.DecimalField(max_digits=10, decimal_places=2)

	image = models.ImageField(upload_to='store_images')

	category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.name
      

# cartmodel
class Cart(models.Model):
    
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        
        return f"{self.user.username}'s Cart"


# Wishlist model (one per user)
class Wishlist(models.Model):
    
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        
        return f"{self.user.username}'s Wishlist"

# Cartitems model
class Cartitems(models.Model):
	
	cart_object = models.ForeignKey(Cart, on_delete=models.CASCADE)

	product_object = models.ForeignKey(Product, on_delete=models.CASCADE)

	quantity = models.PositiveIntegerField(default=1)

	is_ordered = models.BooleanField(default=False)

	def item_total(self):
		return self.product_object.price * self.quantity

	def __str__(self):
		return f"{self.cart_object.user.username} - {self.product_object.name} ({self.quantity})"

# wishlistitem model
class WishlistItem(models.Model):

	wishlist_object = models.ForeignKey(Wishlist, on_delete=models.CASCADE)

	product_object = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.wishlist_object.user.username} - {self.product_object.name}"

# Order model
class Order(models.Model):

    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=15)

    address = models.TextField()

    payment_method = models.CharField(max_length=50, choices=(("COD", "Cash on Delivery"), ("ONLINE", "Online Payment")))

    is_paid = models.BooleanField(default=False)

    order_id = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Order {self.id} by {self.user.username}"

    

# order item 
class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price per unit at purchase time

    def __str__(self):
        
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    @property
    def item_total(self):

        print(self.price * self.quantity)

        return self.price * self.quantity
