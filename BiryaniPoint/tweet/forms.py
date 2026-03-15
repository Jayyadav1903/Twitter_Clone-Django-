from django import forms
from .models import Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets={
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's happening?"}),
        }
        
        
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    