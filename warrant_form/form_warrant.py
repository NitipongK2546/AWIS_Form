from django import forms
from warrant_form.model_reqform import WarrantDataModel
from django.core.exceptions import ValidationError

import datetime
from warrant_form.code_handler import ThaiCountryAreaCode

from django.forms.models import model_to_dict

class WarrantForm(forms.ModelForm):
    class Meta:
        model = WarrantDataModel
        fields = "__all__"
        widgets = {
            "woa_date": forms.DateTimeInput(attrs={'type': 'datetime'}),
            "appointment_date": forms.DateTimeInput(),
        }