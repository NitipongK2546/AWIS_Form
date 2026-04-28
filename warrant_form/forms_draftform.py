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

class FormDraftContainerModelForm(forms.ModelForm):
    class Meta:
        model = FormDraftContainer
        fields = "__all__"

class ReqformDraftModelForm(forms.ModelForm):
    class Meta:
        model = ReqformDraftDataModel
        exclude = ["draft_container",]
        widgets = {
    "req_day": forms.Select(choices=CentralForm.day_choices, attrs={
        'class': 'datehalf day',
    }),
    "req_month": forms.Select(choices=CentralForm.month_choices, attrs={
        'class': 'datehalf month',
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }),
    "req_year": forms.Select(choices=CentralForm.year_choices, attrs={
        'class': 'datehalf year',
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }),
    "scene_date_day": forms.Select(choices=CentralForm.day_choices, attrs={
        'class': 'datehalf day',
    }),
    "scene_date_month": forms.Select(choices=CentralForm.month_choices, attrs={
        'class': 'datehalf month',
        'onchange': 'changeDate(scene_date_day, scene_date_month, scene_date_year)'
    }),
    "scene_date_year": forms.Select(choices=CentralForm.year_choices, attrs={
        'class': 'datehalf year',
        'onchange': 'changeDate(scene_date_day, scene_date_month, scene_date_year)'
    }),
    "woa_start_date_day": forms.Select(choices=CentralForm.day_choices, attrs={
        'class': 'datehalf day',
    }),
    "woa_start_date_month": forms.Select(choices=CentralForm.month_choices, attrs={
        'class': 'datehalf month',
        'onchange': 'changeDate(woa_start_date_day, woa_start_date_month, woa_start_date_year)'
    }),
    "woa_start_date_year": forms.Select(choices=CentralForm.year_choices, attrs={
        'class': 'datehalf year',
        'onchange': 'changeDate(woa_start_date_day, woa_start_date_month, woa_start_date_year)'
    }),
    "woa_end_date_day": forms.Select(choices=CentralForm.day_choices, attrs={
        'class': 'datehalf day',
    }),
    "woa_end_date_month": forms.Select(choices=CentralForm.month_choices, attrs={
        'class': 'datehalf month',
        'onchange': 'changeDate(woa_end_date_day, woa_end_date_month, woa_end_date_year)'
    }),
    "woa_end_date_year": forms.Select(choices=CentralForm.year_choices, attrs={
        'class': 'datehalf year',
        'onchange': 'changeDate(woa_end_date_day, woa_end_date_month, woa_end_date_year)'
    }),
        }

class WarrantDraftDataModelForm(forms.ModelForm):
    class Meta:
        model = WarrantDraftDataModel
        exclude = ["draft_container",]