from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from warrant_form.models import WarrantDataModel
from django.forms.models import model_to_dict
import datetime
from django.utils import timezone
from warrant_form.code_handler import ThaiCountryAreaCode
from uuid import uuid4

class SpecialAWISDataFormModelPartOne(models.Model):
    # POSSIBLY TEMPORARY VARIABLE.
    #req_no = USE ID OF OBJECT INSTEAD.
    court_name = models.CharField(max_length=250, blank=True)
    day = timezone.datetime.today().day
    month = timezone.datetime.today().month
    year = timezone.datetime.today().year

    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = (1, "ทั่วไป")
        DRUGS = (2, "ยาเสพติด")

    court_code = models.CharField(max_length=7, verbose_name="รหัส")

    # We don't even use this in the API
    req_no = models.CharField(max_length=50)
    judge_name = models.CharField(max_length=250)
    req_day = models.PositiveIntegerField()
    req_month = models.PositiveIntegerField()
    # We don't even use this in the API

    req_year = models.PositiveIntegerField()

    req_case_type_id = models.IntegerField(choices=ReqCaseTypeIDChoices) # CHOICES

    police_station_id = models.CharField(max_length=5) #REFER id -> tb_police_station
    req_no_plaintiff = models.CharField(max_length=50)

    plaintiff = models.CharField(max_length=400)
    accused = models.CharField(max_length=400)
    req_name = models.CharField(max_length=300)
    req_pos = models.CharField(max_length=400)
    req_age = models.PositiveIntegerField()

    req_office = models.CharField(max_length=300)
    req_sub_district = models.CharField(max_length=6) # tb_sub_district / sub_district_code
    req_district = models.CharField(max_length=4)
    req_province = models.CharField(max_length=2)

    req_tel = models.CharField(max_length=50)

    # Start of a few unrequired field.
    # cause_type_id 
    cause_type_id_1 = models.BooleanField()
    cause_type_id_2 = models.BooleanField()
    cause_text_1 = models.CharField(max_length=500, blank=True)
    cause_text_2 = models.CharField(max_length=500, blank=True)

    charge = models.CharField(max_length=50, blank=True)
    charge_type_1 = models.BooleanField() 
    charge_type_2 = models.BooleanField()

    scene = models.CharField(max_length=300, blank=True)
    # scene_date_datehalf = models.DateField(blank=True, null=True) 

    class SceneDateMonthChoices(models.IntegerChoices):
        JANUARY = (1, "มกราคม")
        FEBRUARY = (2, "กุมภาพันธ์")
        MARCH = (3, "มีนาคม")
        APRIL = (4, "เมษายน")
        MAY = (5, "พฤษภาคม")
        JUNE = (6, "มิถุนายน")
        JULY = (7, "กรกฎาคม")
        AUGUST = (8, "สิงหาคม")
        SEPTEMBER = (9, "กันยายน")
        OCTOBER = (10, "ตุลาคม")
        NOVEMBER = (11, "พฤศจิกายน")
        DECEMBER = (12, "ธันวาคม")

    scene_date_day = models.PositiveIntegerField(blank=True, null=True)
    scene_date_month = models.PositiveIntegerField(blank=True, null=True)
    scene_date_year = models.PositiveIntegerField(blank=True, null=True)

    scene_date_timehalf = models.TimeField(blank=True, null=True) 
    scene_date = models.CharField(max_length=19, blank=True) 

    act = models.CharField(max_length=500, verbose_name="มีพฤติการกระทำความผิด", blank=True)
    law = models.CharField(max_length=200, verbose_name="ตามกฎหมาย", blank=True)

    court_owner_code = models.CharField(max_length=7, verbose_name="ซึ่งเป็นคดีที่อยู่ในอำนาจศาล", blank=True)

    prescription = models.IntegerField(blank=True, null=True) # อายุความ ปี

    agent_name = models.CharField(max_length=400, blank=True)
    agent_pos = models.CharField(max_length=400, blank=True)

    have_req_1 = models.BooleanField() 
    have_req_2 = models.BooleanField() 

    have_court_code = models.CharField(max_length=7, blank=True) # tb_office court_code
    have_act = models.CharField(max_length=400, blank=True)
    have_injunc = models.CharField(max_length=50, blank=True)

    composer_name = models.CharField(max_length=200, blank=True)
    composer_position = models.CharField(max_length=200, blank=True)
    writer_name = models.CharField(max_length=200, blank=True)
    #############################################
    # THE FILE SAID "write_position" BUT IS IT "write" or "writer"?
    # CHECK LATERRRRRRRRRRRRRRRRR
    writer_position = models.CharField(max_length=200, blank=True)

    create_uid = models.IntegerField()
    #############################################

    #####################################################################3
    # WARRANTS AUTO-FILL SECTION
    acc_full_name = models.CharField(max_length=250)
    acc_card_type = models.IntegerField(blank=True, null=True)
    acc_card_id = models.CharField(max_length=20)
    acc_age = models.IntegerField(blank=True, null=True)
    acc_origin = models.IntegerField(blank=True, null=True)
    acc_nation = models.IntegerField(blank=True, null=True)
    acc_occupation = models.CharField(max_length=100, blank=True)
    acc_addno = models.CharField(max_length=50, blank=True)
    acc_vilno = models.CharField(max_length=50, blank=True)
    acc_road = models.CharField(max_length=100, blank=True)
    acc_soi = models.CharField(max_length=100, blank=True)
    acc_near = models.CharField(max_length=200, blank=True)
    acc_sub_district = models.CharField(max_length=6, blank=True)
    acc_district = models.CharField(max_length=4, blank=True)
    acc_province = models.CharField(max_length=2, blank=True)
    acc_tel = models.CharField(max_length=20, blank=True)

    def toDocumentCompatibleDict(self) -> dict[str, object]:
        """
        Convert the model object into a dictionary that fits what the API required.
        It uses model_to_dict to, first, convert the model into a dictionary with matching field names,
        then convert or remove some fields to match the API.\n
        It is, of course, not JSON object, so don't forget to json.dumps(dict) it later.
        """
        ################################################################
        # Conversion section.
        # Convert dictionary into the format that API can receive.

        dict_main_awis = model_to_dict(self)
        # dict_main_awis.update({"day": self.day})
        # dict_main_awis.update({"month": self.month})
        # dict_main_awis.update({"year": self.year})

        TIMEHALF_STR = "scene_date_timehalf"
        time_half = dict_main_awis.get(TIMEHALF_STR)
        date_half = None
        
        if self.scene_date_year and self.scene_date_month and self.scene_date_day:
            converted_year = self.scene_date_year 
            padded_month = str(self.scene_date_month).zfill(2)
            padded_day = str(self.scene_date_day).zfill(2)

            # The year is already converted from choices -> BE to AD (refer to Form field)
            date_half = f"{converted_year}-{padded_month}-{padded_day}"

        if date_half and time_half:
            # Leave a space between date and time.
            full_datetime = f"{date_half} {time_half}"
            dict_main_awis.update({"scene_date": full_datetime})

        # dict_main_awis.pop("id")
        dict_main_awis.update({"req_no": dict_main_awis.get("id", "NO ID")})

        empty_key_list = []
        for key, value in dict_main_awis.items():
            if isinstance(value, str):
                if not value:
                    empty_key_list.append(key)
            elif isinstance(value, bool):
                if value: # True...
                    dict_main_awis.update({key: 1})
                else:
                    dict_main_awis.update({key: 0})

            if value is None:
                empty_key_list.append(key)

        for key in empty_key_list:
            dict_main_awis.pop(key)

        return dict_main_awis
    
    def toAPICompatibleDict(self) -> dict[str, object]:
        current_dict = self.toDocumentCompatibleDict()
        current_dict.pop("day", None)
        current_dict.pop("month", None)
        current_dict.pop("year", None)

        bool_key_dict : dict[str, int] = {
            "cause_type_id": 2,
            "have_req": 2,
            # "charge_type": 2,
        }
        for bool_key, total_num in bool_key_dict.items():
            bool_value_list = []
            for num in range(total_num):
                # Example: cause_type_id_1
                key = f"{bool_key}_{num + 1}"

                var_value = current_dict.get(key)
                bool_value_list.append((key, var_value))

                current_dict.pop(key, None)

            if bool_value_list[0][1] == 1:
                current_dict.update({bool_key: 0})
            else:
                current_dict.update({bool_key: 1})

        scene_date_year = current_dict.get("scene_date_year")
        scene_date_month = current_dict.get("scene_date_month")
        scene_date_day = current_dict.get("scene_date_day")
        scene_date_timehalf = current_dict.get("scene_date_timehalf")
        combined_date = ""
        if scene_date_year and scene_date_month and scene_date_day:
            converted_year = scene_date_year 
            padded_month = str(scene_date_month).zfill(2)
            padded_day = str(scene_date_day).zfill(2)

            combined_date = f"{converted_year}-{padded_month}-{padded_day}"

            current_dict.pop("scene_date_year")
            current_dict.pop("scene_date_month")
            current_dict.pop("scene_date_day")

        if combined_date and scene_date_timehalf:
            combined_datetime = f"{combined_date} {scene_date_timehalf}"
            current_dict.update({"scene_date": combined_datetime})

            current_dict.pop("scene_date_timehalf")

        current_dict.pop("judge_name")
        current_dict.pop("req_day")
        current_dict.pop("req_month")

        current_dict.pop("acc_full_name")
        current_dict.pop("acc_card_id")
        current_dict.pop("acc_sub_district")
        current_dict.pop("acc_district")
        current_dict.pop("acc_province")
        

        return current_dict

class MainAWISForm(forms.ModelForm):
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

        model = SpecialAWISDataFormModelPartOne
        exclude = ["scene_date"]
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
                'value': 1
            }),
            "police_station_id": forms.HiddenInput(attrs={
                'value': 1
            }),
            "req_no_plaintiff": forms.HiddenInput(attrs={
                'value': 1
            }),
            "create_uid": forms.HiddenInput(attrs={
                'value': 9999
            }),
        }

class WarrantForm(forms.ModelForm):
    class Meta:
        model = WarrantDataModel
        fields = "__all__"
        widgets = {
            "woa_date": forms.DateInput(attrs={'type': 'date'}),
        }