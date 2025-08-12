from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# Custom User Model
class CustomUserModel(AbstractUser):

	username = models.CharField(max_length=150, unique=True)
	
	email = models.EmailField(unique=True)

	phone_number = models.CharField(max_length=15, blank=True)

	gender = models.CharField(max_length=10, choices=(('','Select gender'),('male', 'Male'), ('female', 'Female'), ('other', 'Others')), blank=True)

	def __str__(self):

		return self.username