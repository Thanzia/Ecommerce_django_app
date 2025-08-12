from django import forms
from .models import *

# User Registration Form
class UserRegistrationForm(forms.ModelForm):

	class Meta:

		model = CustomUserModel

		fields = ['username','password','email', 'phone_number', 'gender']

		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}),
			'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
			'gender': forms.Select(attrs={'class': 'form-control'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'})
		}

# Otp Verification Form
class OtpVerificationForm(forms.Form):

    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'}))

# Login Form
class LoginForm(forms.Form):

	username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}))
	
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}))


# Login using Email Form
class LoginEmailForm(forms.Form):

	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}))
	
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}))

# Forgot Password Form
class ForgotPasswordForm(forms.Form):

	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}))

# Reset Password Form
class ResetPasswordForm(forms.Form):

	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter New Password'}))
	
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
