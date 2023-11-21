from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class StockForm(forms.Form):
    choices = [('Buy','Buy'),('Sell','Sell')]
    quantity = forms.IntegerField(max_value=10000,min_value=1)
    order_type = forms.ChoiceField(widget=forms.RadioSelect,choices=choices,label='')
