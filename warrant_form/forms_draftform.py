from django import forms
from .model_draftform import ReqformDraftDataModel, FormDraftContainer, WarrantDraftDataModel

import datetime

from django import forms
from django.core.exceptions import ValidationError

from warrant_form import forms_central as CentralForm
from warrant_form.model_reqform import WarrantDataModel

req_case_type_id_choices = [
    (1, "ทั่วไป"),
    (2, "ยาเสพติด"),
]

class ReqformDraftModelForm(forms.ModelForm):
    class Meta:
        model = ReqformDraftDataModel
        fields = "__all__"

class FormDraftContainerModelForm(forms.ModelForm):
    class Meta:
        model = FormDraftContainer
        exclude = ["reqform",]

class WarrantDraftDataModelForm(forms.ModelForm):
    class Meta:
        model = WarrantDraftDataModel
        fields = "__all__"