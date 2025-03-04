from django.forms import ModelForm
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm

from .models import order,Customer

class OrderForm(ModelForm):
    class Meta:
        model = order
        # fields = '__all__'
        exclude = ['tags']

class customerForm(ModelForm):
    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['user']


class createNewuser(UserCreationForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username','email','password1','password2']
