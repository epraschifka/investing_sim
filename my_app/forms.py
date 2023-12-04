from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Holding

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','password1','password2','money']

class OrderForm(forms.ModelForm):
    class Meta():
        model = Holding
        fields = ['quantity']





