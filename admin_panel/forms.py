# from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from django import forms
from django.db import models

class CustomizedUserCreationForm(UserCreationForm):
    class RoleChoices(models.IntegerChoices):
        OUTSIDE = (0, "Outside")

        EMPLOYEE = (10, "Employee") 
        MANAGER = (11, "Manager")
        DIRECTOR = (12, "Director")

        SYSTEM_ADMIN = (99, "System Admin")

    role = forms.ChoiceField(choices=RoleChoices)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

########################################################



# class UserActiveForm(forms.Form):
#     user = forms.ModelChoiceField(
#         queryset=UserDataModel.objects.all()
#     )
#     is_active = forms.BooleanField(required=False)
