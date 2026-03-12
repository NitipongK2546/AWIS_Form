import datetime

from django import forms
from django.db import models
from django.forms.models import model_to_dict

from warrant_form import forms_central as CentralForm
from warrant_form.model_reqform import WarrantDataModel

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

ACCOUNT_CARD_TYPE_CHOICES = [
    (1, "เลขประจำตัวประชาชน"),
    (2, "เลขหนังสือเดินทาง"),
    (3, "เลขคนซึ่งไม่มีสัญชาติไทย"),
]

def toAPICompatibleDictGeneral(incoming_model : models.Model) -> dict[str, object]:
        """
        Convert the model object into a dictionary that fits what the API required.
        It uses model_to_dict to, first, convert the model into a dictionary with matching field names,
        then convert or remove some fields to match the API.\n
        It is, of course, not JSON object, so don't forget to json.dumps(dict) it later.
        """
        ################################################################
        # Conversion section.
        # Convert dictionary into the format that API can receive.

        model_dict = model_to_dict(incoming_model)

        model_dict.pop("id", None)

        empty_key_list = []
        for key, value in model_dict.items():
            if isinstance(value, str):
                if not value:
                    empty_key_list.append(key)
            elif isinstance(value, bool):
                if value: # True...
                    model_dict.update({key: 1})
                else:
                    model_dict.update({key: 0})

            if value is None:
                empty_key_list.append(key)

        for key in empty_key_list:
            model_dict.update({key: None})

        return model_dict

class WarrantForm(forms.Form):

    court_name = forms.CharField(max_length=250)
    plaintiff = forms.CharField(max_length=400)

    woa_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    woa_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices))
    woa_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices))
    woa_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 

    fault_type_id = forms.IntegerField(widget=forms.Select(choices=FAULT_TYPE_ID_CHOICES)) 
    send_to_name = forms.CharField(max_length=250) # ส่งหมายถึงใคร
    cause_text = forms.CharField(max_length=400) # ด้วย

    charge = forms.CharField(max_length=250)
    charge_type_1 = forms.BooleanField(required=False) 
    charge_type_2 = forms.BooleanField(required=False)
    charge_type_2_1 = forms.BooleanField(required=False)
    charge_type_2_2 = forms.BooleanField(required=False)
    charge_type_2_3 = forms.BooleanField(required=False)
    charge_type_3 = forms.BooleanField(required=False)
    charge_other_text = forms.CharField(max_length=250, required=False)

    acc_full_name_1 = forms.CharField(max_length=250)
    acc_full_name_2 = forms.CharField(max_length=250)

    acc_card_type = forms.IntegerField(required=False, 
    widget=forms.Select(choices=ACCOUNT_CARD_TYPE_CHOICES))
    acc_card_id = forms.CharField(max_length=20)
    # acc_age = forms.IntegerField(required=False, )
    acc_origin = forms.IntegerField(required=False, )
    acc_nation = forms.IntegerField(required=False, )
    acc_occupation = forms.CharField(max_length=100, required=False)
    acc_addno = forms.CharField(max_length=50, required=False)
    acc_vilno = forms.CharField(max_length=50, required=False)
    acc_road = forms.CharField(max_length=100, required=False)
    acc_soi = forms.CharField(max_length=100, required=False)
    acc_near = forms.CharField(max_length=200, required=False)
    acc_sub_district = forms.CharField(max_length=6, required=False, widget=forms.Select(choices=CentralForm.thai_codes.getSubDistrictChoices()[:5]))
    acc_district = forms.CharField(max_length=4, required=False, widget=forms.Select(choices=CentralForm.thai_codes.getDistrictChoices()[:5]))
    acc_province = forms.CharField(max_length=2, required=False, widget=forms.Select(choices=CentralForm.thai_codes.getProvinceChoices()))
    acc_tel = forms.CharField(max_length=20, required=False)

    appointment_type = forms.IntegerField(widget=forms.Select(choices=APPOINTMENT_TYPE_CHOICES), required=False,)
    # appointment_date = models.CharField(max_length=19, required=False, ) # SAME DATE FORMAT AS BELOW

    appointment_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    appointment_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices))
    appointment_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices))
    appointment_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 

    woa_no = forms.IntegerField()
    woa_refno = forms.CharField(max_length=16, required=False)
    woa_type = forms.IntegerField(widget=forms.Select(choices=WOA_TYPE_CHOICES))

    def cleanDateTimeFields(self, current_dict : dict):

        included_fields = ["woa_date", "appointment_date"]

        for field in included_fields:
            current_dict = CentralForm.reattachDateTime(current_dict, field)
    
        return current_dict
    
    def combineDupe(self, current_dict : dict):

        included_fields = ["acc_full_name",]

        for field in included_fields:
            val_num1 = current_dict.get(f"{field}_1")
            val_num2 = current_dict.get(f"{field}_2")

            if val_num1 == val_num2:
                current_dict.update({field: val_num1})
                current_dict.pop(f"{field}_1")
                current_dict.pop(f"{field}_2")
            else:
                raise Exception("VALUE NOT MATCHED.")
        
        return current_dict

    def clean(self):
        cleaned_data = super().clean()

        # cleaned_data.pop("plaintiff", None)
        # cleaned_data.pop("court_name", None)

        self.combineDupe(cleaned_data)
        self.cleanDateTimeFields(cleaned_data)

        return cleaned_data


class DisabledWarrantForm(WarrantForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.disabled = True