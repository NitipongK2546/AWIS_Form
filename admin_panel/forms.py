# from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.db import models

class CustomizedUserCreationForm(UserCreationForm):
    class RoleChoices(models.IntegerChoices):
        EMPLOYEE = (0, "Employee") 
        MANAGER = (1, "Manager")
        DIRECTOR = (2, "Director")
        SYSTEM_ADMIN = (99, "System Admin")

    role = forms.ChoiceField(choices=RoleChoices)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")