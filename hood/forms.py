from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


#usersignup form
class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100,help_text='Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
class UserUpdateForm(forms.ModelForm):
            class Meta:
                model=User
                fields = ['username','email','first_name','last_name']                
       
       
class ProfileUpdateForm(forms.ModelForm):
            class Meta:
                model=Profile
                fields = ['bio','location','hood_name','profile_pic']        