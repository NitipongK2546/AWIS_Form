from django import forms
from users.models import UserDataModel

class OwnershipForm(forms.Form):
    form_creator = forms.ModelChoiceField(
        UserDataModel.objects.all()
    )
    form_owner = forms.ModelChoiceField(
        UserDataModel.objects.all()
    )