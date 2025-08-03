from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .constants import *

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Role.choices, required=True, initial=Role.INVENTORY)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", 'user_type')
