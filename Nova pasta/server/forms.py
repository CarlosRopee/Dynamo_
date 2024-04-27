from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField(max_length=254, required=True, help_text='Enter a valid email address.')
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']