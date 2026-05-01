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
    "req_case_type_id": forms.Select(choices=req_case_type_id_choices),
    "woa_start_date": forms.DateTimeInput(attrs={
        'class': 'datetimepicker',
        'placeholder': "เลือกวันที่และเวลา"
    }),
    "woa_end_date": forms.DateTimeInput(attrs={
        'class': 'datetimepicker',
        'placeholder': "เลือกวันที่และเวลา"
    }),
    "req_sub_district": forms.Select(
        choices=CentralForm.thai_codes.getSubDistrictChoices()[:5]
    ),
    "req_district": forms.Select(
        choices=CentralForm.thai_codes.getDistrictChoices()[:5]
    ),
    "req_province": forms.Select(
        choices=CentralForm.thai_codes.getProvinceChoices()
    ),
    "acc_sub_district": forms.Select(
        choices=CentralForm.thai_codes.getSubDistrictChoices()[:5]
    ),
    "acc_district": forms.Select(
        choices=CentralForm.thai_codes.getDistrictChoices()[:5]
    ),
    "acc_province": forms.Select(
        choices=CentralForm.thai_codes.getProvinceChoices()
    ),
    "acc_origin": forms.Select(
        choices=CentralForm.nation_codes.getChoices()
    ),
    "acc_nation": forms.Select(
        choices=CentralForm.nation_codes.getChoices()
    ),
    "court_code": forms.Select(
        choices=CentralForm.court_codes.getChoices()
    ),
    "have_court_code": forms.Select(
        choices=CentralForm.court_codes.getChoices()
    ),
    "court_owner_code": forms.Select(
        choices=CentralForm.court_codes.getChoices()
    ),
    "have_req": forms.Select(
        choices=(
            (0, "ไม่เคย"),
            (1, "เคย")
        )
    ),
    "cause_type_id": forms.Select(
        choices=(
            (1, "ร้องทุกข์"),
            (2, "สืบสวนสอบสวน")
        )
    ),
}
        
WOA_TYPE_CHOICES = [
    (1, "47"),
    (2, "47 ทวิ"),
]

FAULT_TYPE_ID_CHOICES = [
    (1, "แพ่ง"),
    (2, "อาญา"),
]

APPOINTMENT_TYPE_CHOICES = [
    (1, "กำหนดอายุความ"),
    (2, "กำหนดนัด")
]

class WarrantDraftDataModelForm(forms.ModelForm):
    class Meta:
        model = WarrantDraftDataModel
        exclude = ["draft_container", "court_name", "plaintiff"]
        widgets = {
    "acc_sub_district": forms.Select(
        choices=CentralForm.thai_codes.getSubDistrictChoices()[:5]
    ),
    "acc_district": forms.Select(
        choices=CentralForm.thai_codes.getDistrictChoices()[:5]
    ),
    "acc_province": forms.Select(
        choices=CentralForm.thai_codes.getProvinceChoices()
    ),
    "acc_origin": forms.Select(
        choices=CentralForm.nation_codes.getChoices()
    ),
    "acc_nation": forms.Select(
        choices=CentralForm.nation_codes.getChoices()
    ),
    "woa_date": forms.DateTimeInput(attrs={
        'class': 'datetimepicker',
        'placeholder': "เลือกวันที่และเวลา"
    }),
    "appointment_date": forms.DateTimeInput(attrs={
        'class': 'datetimepicker',
        'placeholder': "เลือกวันที่และเวลา"
    }),
    "woa_type": forms.Select(
        choices=WOA_TYPE_CHOICES,
    ),
    "fault_type_id": forms.Select(
        choices=FAULT_TYPE_ID_CHOICES
    ),
    "appointment_type": forms.Select(
        choices=APPOINTMENT_TYPE_CHOICES
    ),
        }