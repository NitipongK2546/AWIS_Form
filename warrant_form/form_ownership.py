from django import forms
from users.models import UserDataModel

ALL_USER = UserDataModel.objects.all()

class OwnershipForm(forms.Form):
    form_creator = forms.ModelChoiceField(ALL_USER)
    form_owner = forms.ModelChoiceField(ALL_USER)