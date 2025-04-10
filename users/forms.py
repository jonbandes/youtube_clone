from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    """
    Custom user registration form extending Django's UserCreationForm.
    
    Adds:
        - Email (required)
        - Profile picture (optional)
        - Bio (optional)
    """
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'bio']