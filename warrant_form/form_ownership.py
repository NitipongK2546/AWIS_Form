from django import forms
from users.models import UserDataModel

class OwnershipForm(forms.Form):
    form_creator = forms.ModelChoiceField(
        UserDataModel.objects.filter(api_uid__gte=0)
    )
    form_owner = forms.ModelChoiceField(
        UserDataModel.objects.filter(api_uid__gte=0)
    )