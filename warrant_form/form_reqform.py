import datetime

from django import forms
from django.core.exceptions import ValidationError

from warrant_form import forms_central as CentralForm
from warrant_form.model_reqform import WarrantDataModel

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
    
    req_day = forms.IntegerField(widget=forms.Select(choices=CentralForm.day_choices))
    req_month = forms.IntegerField(widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(req_day, req_month)'
    }))
    req_year = forms.IntegerField(widget=forms.Select(choices=CentralForm.year_choices))

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
    req_sub_district = forms.CharField(max_length=6, widget=forms.Select(choices=CentralForm.thai_codes.getSubDistrictChoices())) # tb_sub_district / sub_district_code
    req_district = forms.CharField(max_length=4, widget=forms.Select(choices=CentralForm.thai_codes.getDistrictChoices()))
    req_province = forms.CharField(max_length=2, widget=forms.Select(choices=CentralForm.thai_codes.getProvinceChoices()))
    req_tel = forms.CharField(max_length=50)

    # Start of a few unrequired field.
    # cause_type_id 
    cause_type_id_1 = forms.BooleanField(required=False)
    cause_type_id_2 = forms.BooleanField(required=False)
    cause_text_1 = forms.CharField(max_length=500, required=False)
    cause_text_2 = forms.CharField(max_length=500, required=False)

    charge = forms.CharField(max_length=50, required=False, widget=forms.Textarea(attrs={
                'style':'resize:none;'
            }), )
    charge_type_1 = forms.BooleanField(required=False) 
    charge_type_2 = forms.BooleanField(required=False)

    scene = forms.CharField(max_length=300, required=False, widget=forms.Textarea(attrs={
                'style':'resize:none;'
            }), )
    # scene_date_datehalf = forms.DateField(required=False, ) 

    scene_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    scene_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(scene_date_day, scene_date_month)'
    }))
    scene_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices))

    scene_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 
    # scene_date = forms.CharField(max_length=19, required=False) 

    act = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
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

    woa_start_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    woa_start_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(woa_start_date_day, woa_start_date_month)'
    }))
    woa_start_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices))

    woa_start_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={
        'type': 'time',
        })) 

    woa_end_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    woa_end_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(woa_end_date_day, woa_end_date_month)'
    }))
    woa_end_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices))

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
    acc_sub_district = forms.CharField(max_length=6, required=False, widget=forms.Select(choices=CentralForm.thai_codes.getSubDistrictChoices()))
    acc_district = forms.CharField(max_length=4, required=False, widget=forms.Select(choices=CentralForm.thai_codes.getDistrictChoices()))
    acc_province = forms.CharField(max_length=2, required=False, widget=forms.Select(choices=CentralForm.thai_codes.getProvinceChoices()))
    acc_tel = forms.CharField(max_length=20, required=False)

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
            current_dict = CentralForm.reattachDateTime(current_dict, field)
        
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

class DisabledFormStep1(AWISFormStep1):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.disabled = True