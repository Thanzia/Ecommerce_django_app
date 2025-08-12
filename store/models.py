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


