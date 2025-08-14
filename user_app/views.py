
from django.shortcuts import render,redirect
from django.views.generic import View

from user_app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.conf import settings
from django.http import HttpResponse

from user_app.models import *
from store.models import *

import random

# # Create your views here.
# # 1.UserregistrationView
# # methods:get,post

class UserRegistrationView(View):

	def get(self,request):

		form = UserRegistrationForm

		return render(request,"signup.html",{"form":form})

	def post(self,request):

		form = UserRegistrationForm(request.POST)

		if form.is_valid():

			email = form.cleaned_data.get('email')

			otp = random.randint(1000,9999)

			request.session['otp'] = otp

			request.session['username'] = form.cleaned_data.get('username')

			request.session['password'] = form.cleaned_data.get('password')

			request.session['email'] = form.cleaned_data.get('email')

			request.session['phone_number'] = form.cleaned_data.get('phone_number')

			request.session['gender'] = form.cleaned_data.get('gender')

	
			send_mail(subject="Otp for verification",message=str(otp),from_email=settings.EMAIL_HOST_USER,
			          recipient_list=[email],fail_silently=False)
			
			return redirect("otp_verify") 
			
		return render(request,"signup.html",{"form":form})
	
# 2.otpverificationview
# methods:get,post

class OtpVerificationView(View):

	def get(self,request):

		form = OtpVerificationForm

		return render(request,"otpverify.html",{"form":form})
	
	def post(self,request):

		form = OtpVerificationForm(request.POST)

		if form.is_valid():

			otp_entered = form.cleaned_data.get('otp')

			otp_stored = request.session.get('otp')

			if int(otp_entered) == int(otp_stored):

				print("otp matches")

				username = request.session.get('username')

				email = request.session.get('email')

				password = request.session.get('password')

				phone_number = request.session.get('phone_number')

				gender = request.session.get('gender')

				user = CustomUserModel.objects.create_user(username=username,email=email,password=password,phone_number=phone_number,gender=gender)

				Cart.objects.create(user=user)

				Wishlist.objects.create(user=user)

				print("successful")

				return redirect("login")
		
		return render(request,"otpverify.html",{"form":form})
	
# LoginView using username

class LoginView(View):

	def get(self,request):

		form = LoginForm

		return render(request,"login.html",{"form":form})
	
	def post(self,request):

		form = LoginForm(request.POST)

		if form.is_valid():

			username = form.cleaned_data.get('username')

			password = form.cleaned_data.get('password')

			user_obj = authenticate(request,username=username,password=password)

			if user_obj:

				login(request,user_obj)

				print("login successful")

				return redirect("products_list")
			
			form = LoginForm
			
			return render(request,"login.html",{"form":form})
		
		
# Login using email

class LoginEmailView(View):

	def get(self,request):

		form = LoginEmailForm

		return render(request,"login_email.html",{"form":form})
	
	def post(self,request):

		form = LoginEmailForm(request.POST)

		if form.is_valid():

			email = form.cleaned_data.get('email')

			password = form.cleaned_data.get('password')

			user = CustomUserModel.objects.get(email=email)

			user_obj = authenticate(request,username=user.username,password=password)

			if user_obj:

				login(request,user_obj)

				return redirect("products_list")
				# print("login successful")
		
		return render(request,"login_email.html",{"form":form}) 
	


# logoutview

class LogoutView(View):

	def get(self,request):

		logout(request)

		return redirect("login")
	
# forgotpasswordview

class ForgotPasswordView(View):

	def get(self,request):

		form = ForgotPasswordForm

		return render(request,"forgotpwd.html",{"form":form})
	
	def post(self,request):

		form = ForgotPasswordForm(request.POST)

		if form.is_valid():

			email = form.cleaned_data.get('email')

			otp = random.randint(1000,9999)

			request.session['otp'] = otp

			user = CustomUserModel.objects.get(email=email)

			request.session['username'] = user.username

			print(user)

			send_mail(subject="Otp for forgot password",message=str(otp),from_email=settings.EMAIL_HOST_USER,
			          recipient_list=[email],fail_silently=False)

			return redirect("pwdotp_verify")
		
		return render(request,"forgotpwd.html",{"form":form})

# OtpverifyView

class OtpVerifyView(View):

	def get(self,request):

		form = OtpVerificationForm

		return render(request,"otp_verify_pwd.html",{"form":form})
	
	def post(self,request):

		form = OtpVerificationForm(request.POST)

		if form.is_valid():

			otp_stored = request.session.get('otp')

			otp_entered = form.cleaned_data.get('otp')

			if int(otp_stored) == int(otp_entered):

				print("success")

				return redirect("reset_pwd")
			

		return render(request,"otp_verify_pwd.html",{"form":form})
	
# resetpasswordview

class ResetPasswordView(View):

	def get(self,request):

		form = ResetPasswordForm

		return render(request,"reset_pwd.html",{"form":form})
	
	def post(self,request):

		form = ResetPasswordForm(request.POST)

		print(request.POST)

		if form.is_valid():

			print("Form is valid")

			password = form.cleaned_data.get('password')

			confirm_password = form.cleaned_data.get('confirm_password')

			if password == confirm_password:

				print("Passwords match")

				username = request.session.get('username')

				user = CustomUserModel.objects.get(username=username)

				user.set_password(password)

				user.save()
				print("Password reset successful")

				return redirect("login")
		
		return render(request,"reset_pwd.html",{"form":form}) 
			


class BaseView(View):

	def get(self,request):

		return render(request,"base.html")

class IndexView(View):

	def get(self,request):

		query = request.GET.get('q')
		
		if query:
			
			if Product.objects.filter(name__iexact=query):
				
				products = Product.objects.filter(name__iexact=query)
				
				return render(request,"index.html",{"products":products})
			
			else:
				
				products = Product.objects.all()
				
				return render(request,"index.html",{"products":products})
			
			
		products = Product.objects.all()
		
		return render(request,"index.html",{"products":products})
	

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def faq_view(request):
    return render(request, 'faq.html')

def returns_view(request):
    return render(request, 'returns.html')

def shipping_view(request):
    return render(request, 'shipping.html')

def careers_view(request):
    return render(request, 'careers.html')

def privacy_view(request):
	return render(request, 'privacy.html')

