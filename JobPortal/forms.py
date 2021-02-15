from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

'''class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField()    
    class Meta:
        model = user2
        fields = ['username','email','dob','gender','mobile','password1', 'password2']'''
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio','gender','dob','mobile','resume']

class ApplyForm(ModelForm):
    class Meta:
        model=Candidates
        fields = ['dob','gender','mobile','resume']

class postForm(ModelForm):
    class Meta:
        model=Company
        fields = "__all__"  
