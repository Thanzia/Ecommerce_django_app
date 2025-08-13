from django import forms
from store.models import *

# Order Form
class OrderForm(forms.ModelForm):
    
    class Meta:
        
        model = Order
        
        fields = ['name', 'phone_number', 'address', 'payment_method']