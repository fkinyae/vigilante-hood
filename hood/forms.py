from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput, TextInput, Textarea
from .models import Profile, NeighbourHood


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
                
class NeighbourHoodForm(forms.ModelForm):
    class Meta:
        model = NeighbourHood
        exclude = ('admin',)   
        fields = ['hood_pic', 'name', 'locality', 'occupants_count', 'police_call', 'hospital_call', 'Fire_call' ]   
        
        widgets = {
            'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'name of neighbourhood'}),
            'locality' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Location'}),
            'occupants_count' : NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Occupants Count'}),
            'police_call' : NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Police Department'}),
            'hospital_call' : NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Hospital Contact'}),
            'Fire_call' : NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Fire Department Tel.'}),





        }
    