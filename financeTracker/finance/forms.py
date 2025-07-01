from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import transactions,Goal

class transactionForm(forms.ModelForm):
    class Meta:
        model = transactions
        fields = ["title","amount","transaction_type","category",'date']

class goalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [ "name","target_amount","deadline"]

class RegisterForm(UserCreationForm):
    #email field not present inside the user, hence used 
    email=forms.EmailField
    class Meta:
        model=User
        fields=['username','email','password1','password2']


        