from django import forms
from django.core.exceptions import ValidationError
from warrant_form.test_models import WarrantDataModel, MainAWISDataModel

from warrant_form.model_reqform import ReqformDataModel
from warrant_form.model_reqform import WarrantDataModel

import datetime
from django.utils import timezone
from warrant_form.code_handler import ThaiCountryAreaCode
from uuid import uuid4

class AWISFormStep1(forms.ModelForm):
    def clean_date(self, data : dict[str, object]):
        combined_date = ""
        try:
            scene_date_year = data.get("scene_date_year")
            scene_date_month = data.get("scene_date_month")
            scene_date_day = data.get("scene_date_day")
            if scene_date_year and scene_date_month and scene_date_day:
            # BUDDHIST_ERA_YEAR_DIFF = 543
                converted_year = scene_date_year 
                padded_month = str(scene_date_month).zfill(2)
                padded_day = str(scene_date_day).zfill(2)

                combined_date = f"{converted_year}-{padded_month}-{padded_day}"
                datetime.date.fromisoformat(combined_date)

            # One of the field doesn't exist.
        except:
            self.add_error(f"Invalid Date: {combined_date}")
        
    def clean_multi_boolean(self, data : dict[str, object]):
        bool_key_dict : dict[str, int] = {
            "cause_type_id": 2,
            "have_req": 2,
            # "charge_type": 2,
        }
        # This is for checking -> If one is True, the other must be False.
        for bool_key, total_num in bool_key_dict.items():
            bool_value_list = []
            for num in range(total_num):
                # Example: cause_type_id_1
                key = f"{bool_key}_{num + 1}"

                var_value = data.get(key)
                bool_value_list.append(var_value)
            # Check if multiple checkboxes was ticked.
            # More than 1 = impossible, raise error.
            if bool_value_list.count(1) > 1:
                for num in range(total_num):
                    key = f"{bool_key}_{num + 1}"
                    custom_error = ValidationError(f"Duplicated Checkboxes from the same type.")
                    self.add_error(key, custom_error)

    def clean(self):
        cleaned_data = super().clean()
        self.clean_date(cleaned_data)
        self.clean_multi_boolean(cleaned_data)

        return cleaned_data
    
    class Meta:
        today_year = datetime.date.today().year
        year_choices = [(year, year + 543) for year in range(1970, today_year + 1)]
        day_choices = [(day, day) for day in range(1, 31 + 1)]
        month_choices = [
            (1, "มกราคม"),
            (2, "กุมภาพันธ์"),
            (3, "มีนาคม"),
            (4, "เมษายน"),
            (5, "พฤษภาคม"),
            (6, "มิถุนายน"),
            (7, "กรกฎาคม"),
            (8, "สิงหาคม"),
            (9, "กันยายน"),
            (10, "ตุลาคม"),
            (11, "พฤศจิกายน"),
            (12, "ธันวาคม"),
        ]
        thai_codes = ThaiCountryAreaCode()

        model = ReqformDataModel
        exclude = ["warrants",]
        widgets = {
            'req_year': forms.Select(choices=year_choices),
            'req_day': forms.Select(choices=day_choices,),
            'req_month': forms.Select(choices=month_choices, attrs={
                'onchange': "adjustDate()"
            }),
            'acc_province': forms.Select(choices=thai_codes.getProvinceChoices()),
            'acc_district': forms.Select(choices=thai_codes.getDistrictChoices()),
            'acc_sub_district': forms.Select(choices=thai_codes.getSubDistrictChoices()),
            'req_province': forms.Select(choices=thai_codes.getProvinceChoices()),
            'req_district': forms.Select(choices=thai_codes.getDistrictChoices()),
            'req_sub_district': forms.Select(choices=thai_codes.getSubDistrictChoices()),
            'scene_date_timehalf': forms.TimeInput(attrs={'type': 'time'}),
            'scene_date_year': forms.Select(choices=year_choices),
            'scene_date_day': forms.Select(choices=day_choices,),
            'scene_date_month': forms.Select(choices=month_choices, attrs={
                'onchange': "adjustDate()"
            }),
            'scene': forms.Textarea(attrs={
                'rows': 5,
                'cols': 135,
                'style':'resize:none;'
            }), 
            'act': forms.Textarea(attrs={
                'rows': 5,
                'cols': 135,
                'style':'resize:none;'
            }),
            'charge': forms.Textarea(attrs={
                'rows': 5,
                'cols': 135,
                'style':'resize:none;'
            }),
            "court_code": forms.HiddenInput(attrs={
                'value': "0000011"
            }),
            "police_station_id": forms.HiddenInput(attrs={
                'value': "TCCT0001"
            }),
            "req_no_plaintiff": forms.HiddenInput(attrs={
                'value': "tcctd20260304002"
            }),
            "create_uid": forms.HiddenInput(attrs={
                'value': 10000010
            }),
        }

class MainAWISForm(forms.ModelForm):
    class Meta:
        model = MainAWISDataModel
        # fields = "__all__"
        exclude = ["warrants",]
        widgets = {
            "scene_date": forms.DateTimeInput(),
        }

class WarrantForm(forms.ModelForm):
    class Meta:
        model = WarrantDataModel
        fields = "__all__"
        widgets = {
            "woa_date": forms.DateInput(attrs={'type': 'date'}),
            "woa_start_date": forms.DateInput(attrs={'type': 'date'}),
            "woa_end_date": forms.DateInput(attrs={'type': 'date'}),
            "appointment_date": forms.DateTimeInput(),
        }