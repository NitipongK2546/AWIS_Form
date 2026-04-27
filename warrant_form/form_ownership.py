from django import forms
from users.models import UserDataModel

class OwnershipForm(forms.Form):
    # form_creator = forms.ModelChoiceField(ALL_USER)
    form_owner = forms.ModelChoiceField(
        UserDataModel.objects.all()
    )