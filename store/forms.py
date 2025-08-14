from django import forms
from store.models import *

# Order Form
class OrderForm(forms.ModelForm):
    
    class Meta:
        
        model = Order
        
        fields = ['name', 'phone_number', 'address', 'payment_method']

        labels = {

            'payment_method': 'Select Your Payment Method',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }