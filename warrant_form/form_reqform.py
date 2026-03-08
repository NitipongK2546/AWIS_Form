from django import forms
from warrant_form.model_reqform import WarrantDataModel
from django.core.exceptions import ValidationError

import datetime
from warrant_form.code_handler import ThaiCountryAreaCode

from django.forms.models import model_to_dict

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

req_case_type_id_choices = [
    (1, "ทั่วไป"),
    (2, "ยาเสพติด"),
]

class AWISFormStep1(forms.Form):
    court_code = forms.CharField(max_length=7, widget=forms.HiddenInput())
    police_station_id = forms.CharField(max_length=8, widget=forms.HiddenInput())
    req_no_plaintiff = forms.CharField(max_length=50, widget=forms.HiddenInput())
    create_uid = forms.IntegerField(widget=forms.HiddenInput())

    reqno = forms.CharField(max_length=50, required=False,)
    # เป็นการผสมกันระหว่าง case_type_id, req_form_number, และ req_year

    req_form_number = forms.IntegerField()
    
    req_day = forms.IntegerField(widget=forms.Select(choices=day_choices))
    req_month = forms.IntegerField(widget=forms.Select(choices=month_choices))
    req_year = forms.IntegerField(widget=forms.Select(choices=year_choices))

    req_case_type_id = forms.IntegerField(widget=forms.Select(choices=req_case_type_id_choices))

    court_name_1 = forms.CharField(max_length=250, required=False)
    court_name_2 = forms.CharField(max_length=250, required=False)
    court_code = forms.CharField(max_length=7,)

    judge_name = forms.CharField(max_length=250)

    police_station_id = forms.CharField(max_length=8) #REFER id -> tb_police_station
    req_no_plaintiff = forms.CharField(max_length=50)

    plaintiff_1 = forms.CharField(max_length=400)
    plaintiff_2 = forms.CharField(max_length=400)
    accused_1 = forms.CharField(max_length=400)
    accused_2 = forms.CharField(max_length=400)
    
    req_name = forms.CharField(max_length=300)
    req_pos = forms.CharField(max_length=400)
    req_age = forms.IntegerField()

    req_office = forms.CharField(max_length=300)
    req_sub_district = forms.CharField(max_length=6, widget=forms.Select(choices=thai_codes.getSubDistrictChoices())) # tb_sub_district / sub_district_code
    req_district = forms.CharField(max_length=4, widget=forms.Select(choices=thai_codes.getDistrictChoices()))
    req_province = forms.CharField(max_length=2, widget=forms.Select(choices=thai_codes.getProvinceChoices()))
    req_tel = forms.CharField(max_length=50)

    # Start of a few unrequired field.
    # cause_type_id 
    cause_type_id_1 = forms.BooleanField(required=False)
    cause_type_id_2 = forms.BooleanField(required=False)
    cause_text_1 = forms.CharField(max_length=500, required=False)
    cause_text_2 = forms.CharField(max_length=500, required=False)

    charge = forms.CharField(max_length=50, required=False, widget=forms.Textarea(attrs={
                'rows': 5,
                'cols': 135,
                'style':'resize:none;'
            }), )
    charge_type_1 = forms.BooleanField(required=False) 
    charge_type_2 = forms.BooleanField(required=False)

    scene = forms.CharField(max_length=300, required=False, widget=forms.Textarea(attrs={
                'rows': 5,
                'cols': 135,
                'style':'resize:none;'
            }), )
    # scene_date_datehalf = forms.DateField(required=False, ) 

    scene_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=day_choices))
    scene_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=month_choices))
    scene_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=year_choices))

    scene_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 
    # scene_date = forms.CharField(max_length=19, required=False) 

    act = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
                'rows': 5,
                'cols': 135,
                'style':'resize:none;'
            }), )
    law = forms.CharField(max_length=200, required=False)

    court_owner_code = forms.CharField(max_length=7, required=False)

    prescription = forms.IntegerField(required=False, ) # อายุความ ปี

    agent_name = forms.CharField(max_length=400, required=False)
    agent_pos = forms.CharField(max_length=400, required=False)

    have_req_1 = forms.BooleanField(required=False) 
    have_req_2 = forms.BooleanField(required=False) 

    have_court_code = forms.CharField(max_length=7, required=False) # tb_office court_code
    have_act = forms.CharField(max_length=400, required=False)
    have_injunc = forms.CharField(max_length=50, required=False)

    composer_name = forms.CharField(max_length=200, required=False)
    composer_position = forms.CharField(max_length=200, required=False)
    writer_name = forms.CharField(max_length=200, required=False)
    write_position = forms.CharField(max_length=200, required=False)

    create_uid = forms.IntegerField()

    #######################

    woa_start_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=day_choices))
    woa_start_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=month_choices))
    woa_start_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=year_choices))

    woa_start_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 


    woa_end_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=day_choices))
    woa_end_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=month_choices))
    woa_end_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=year_choices))

    woa_end_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 


    #############################################

    #####################################################################3
    # WARRANTS AUTO-FILL SECTION
    acc_full_name = forms.CharField(max_length=250)
    acc_card_type = forms.IntegerField(required=False, )
    acc_card_id = forms.CharField(max_length=20)
    acc_age = forms.IntegerField(required=False, )
    acc_origin = forms.IntegerField(required=False, )
    acc_nation = forms.IntegerField(required=False, )
    acc_occupation = forms.CharField(max_length=100, required=False)
    acc_addno = forms.CharField(max_length=50, required=False)
    acc_vilno = forms.CharField(max_length=50, required=False)
    acc_road = forms.CharField(max_length=100, required=False)
    acc_soi = forms.CharField(max_length=100, required=False)
    acc_near = forms.CharField(max_length=200, required=False)
    acc_sub_district = forms.CharField(max_length=6, required=False, widget=forms.Select(choices=thai_codes.getSubDistrictChoices()))
    acc_district = forms.CharField(max_length=4, required=False, widget=forms.Select(choices=thai_codes.getDistrictChoices()))
    acc_province = forms.CharField(max_length=2, required=False, widget=forms.Select(choices=thai_codes.getProvinceChoices()))
    acc_tel = forms.CharField(max_length=20, required=False)

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

        dict_main_awis.pop("id")

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
            dict_main_awis.update({key: None})

        return dict_main_awis
    
    def toAPICompatibleDict(self,) -> dict[str, object]:
        current_dict = self.toDocumentCompatibleDict()
        current_dict.pop("day", None)
        current_dict.pop("month", None)
        current_dict.pop("year", None)

        bool_key_dict : dict[str, int] = {
            "cause_type_id": 2,
            "have_req": 2,
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

        current_dict.pop("req_day")
        current_dict.pop("req_month")

        current_dict.pop("acc_full_name")
        current_dict.pop("acc_card_id")
        current_dict.pop("acc_sub_district")
        current_dict.pop("acc_district")
        current_dict.pop("acc_province")

        return current_dict
    
    
    def toAPICompatibleDictWithConvertedWarrants(self, prefix : str = None) -> dict[str, object]:
        cleaned_dict = self.toAPICompatibleDict()

        warrants_obj = self.warrants.all()
        warrants_list = [item.toAPICompatibleDict() for item in warrants_obj]

        if prefix:
            cleaned_dict.update({f"{prefix}_warrants": warrants_list})
            return cleaned_dict
        
        cleaned_dict.update({f"warrants": warrants_list})
        return cleaned_dict
    
################################################################################

    def clean_date(self, data : dict[str, object]):

        included_fields = ["scene_date", "woa_start_date", "woa_end_date"]

        try:
            for field in included_fields:
                scene_date_year = data.get(f"{field}_year")
                scene_date_month = data.get(f"{field}_month")
                scene_date_day = data.get(f"{field}_day")
                if scene_date_year and scene_date_month and scene_date_day:
                # BUDDHIST_ERA_YEAR_DIFF = 543
                    converted_year = scene_date_year 
                    padded_month = str(scene_date_month).zfill(2)
                    padded_day = str(scene_date_day).zfill(2)

                    combined_date = f"{converted_year}-{padded_month}-{padded_day}"
                    datetime.date.fromisoformat(combined_date)

                # timehalf = data.get(f"{field}_timehalf")
                # data.update({f"{field}_timehalf": datetime.time.strftime(timehalf, "HH:MM:SS")})
                # data.pop(f"{field}_timehalf", None)

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

    def combineDupe(self, current_dict : dict):

        included_fields = ["plaintiff", "accused", "court_name"]

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
    
    def cleanDateTimeFields(self, current_dict : dict):

        included_fields = ["scene_date", "woa_start_date", "woa_end_date"]

        for field in included_fields:
            current_dict = reattachDateTime(current_dict, field)
        
        return current_dict

    def clean(self):
        cleaned_data = super().clean()
        self.clean_date(cleaned_data)
        self.clean_multi_boolean(cleaned_data)
        self.combineDupe(cleaned_data)
        self.cleanDateTimeFields(cleaned_data)

        case_type_text = {
            1: "จ.",
            2: "ยจ.",
        }

        req_case_type_id = cleaned_data.get("req_case_type_id")
        req_form_number = cleaned_data.get("req_form_number")
        req_year = cleaned_data.get("req_year")
        
        # Thus, reqno is buddhist year, while stored year is iso year.
        if req_case_type_id and req_form_number and req_year:
            buddhist_year = req_year + 543
            reqno = f"{case_type_text.get(req_case_type_id)}{req_form_number}/{buddhist_year}"

            cleaned_data.update({"reqno": reqno})

        return cleaned_data

def reattachDateTime(current_dict : dict, field : str):
        
    scene_date_year = current_dict.get(f"{field}_year")
    scene_date_month = current_dict.get(f"{field}_month")
    scene_date_day = current_dict.get(f"{field}_day")
    scene_date_timehalf = current_dict.get(f"{field}_timehalf")
    combined_date = ""
    combined_datetime = "1970-01-01 00:00:00"
    if scene_date_year and scene_date_month and scene_date_day:
        converted_year = scene_date_year 
        padded_month = str(scene_date_month).zfill(2)
        padded_day = str(scene_date_day).zfill(2)

        combined_date = f"{converted_year}-{padded_month}-{padded_day}"

    if combined_date and scene_date_timehalf:
        combined_datetime = f"{combined_date} {scene_date_timehalf}"

    current_dict.pop(f"{field}_year", None)
    current_dict.pop(f"{field}_month", None)
    current_dict.pop(f"{field}_day", None)
    current_dict.pop(f"{field}_timehalf", None)

    current_dict.update({f"{field}": combined_datetime})

    return current_dict