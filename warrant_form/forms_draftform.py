from django import forms
from .model_draftform import ReqformDraftDataModel

import datetime

from django import forms
from django.core.exceptions import ValidationError

from warrant_form import forms_central as CentralForm
from warrant_form.model_reqform import WarrantDataModel

req_case_type_id_choices = [
    (1, "ทั่วไป"),
    (2, "ยาเสพติด"),
]

# class ReqformDraftModelForm(forms.ModelForm):
#     class Meta:
#         model = ReqformDraftDataModel
#         fields = "__all__"

class ReqformDraftModelForm(forms.Form):
    court_code = forms.CharField(required=False,max_length=7, widget=forms.HiddenInput())
    police_station_id = forms.CharField(required=False,max_length=8, widget=forms.HiddenInput())
    req_no_plaintiff = forms.CharField(required=False,max_length=50, widget=forms.HiddenInput())
    create_uid = forms.IntegerField(required=False,widget=forms.HiddenInput())

    reqno = forms.CharField(required=False,max_length=50, )
    # เป็นการผสมกันระหว่าง case_type_id, req_form_number, และ req_year

    req_form_number = forms.IntegerField(required=False,)
    
    req_day = forms.IntegerField(required=False,widget=forms.Select(choices=CentralForm.day_choices))
    req_month = forms.IntegerField(required=False,widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }))
    req_year = forms.IntegerField(required=False,widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }))

    req_case_type_id = forms.IntegerField(required=False,widget=forms.Select(choices=req_case_type_id_choices))

    court_name_1 = forms.CharField(required=False,max_length=250, )
    court_name_2 = forms.CharField(required=False,max_length=250, )
    court_code = forms.CharField(required=False,max_length=7,)

    judge_name = forms.CharField(required=False,max_length=250, )

    police_station_id = forms.CharField(required=False,max_length=8) #REFER id -> tb_police_station
    req_no_plaintiff = forms.CharField(required=False,max_length=50)

    plaintiff_1 = forms.CharField(required=False,max_length=400)
    plaintiff_2 = forms.CharField(required=False,max_length=400)
    accused_1 = forms.CharField(required=False,max_length=400)
    accused_2 = forms.CharField(required=False,max_length=400)
    
    req_name = forms.CharField(required=False,max_length=300)
    req_pos = forms.CharField(required=False,max_length=400)
    req_age = forms.IntegerField(required=False,)

    req_office = forms.CharField(required=False,max_length=300)
    req_sub_district = forms.CharField(required=False,max_length=6, widget=forms.Select(choices=CentralForm.thai_codes.getSubDistrictChoices()[:5])) # tb_sub_district / sub_district_code
    req_district = forms.CharField(required=False,max_length=4, widget=forms.Select(choices=CentralForm.thai_codes.getDistrictChoices()[:5]))
    req_province = forms.CharField(required=False,max_length=2, widget=forms.Select(choices=CentralForm.thai_codes.getProvinceChoices()))
    req_tel = forms.CharField(required=False,max_length=50)

    # Start of a few unrequired field.
    # cause_type_id 
    cause_type_id_1 = forms.BooleanField(required=False,)
    cause_type_id_2 = forms.BooleanField(required=False,)
    cause_text_1 = forms.CharField(required=False,max_length=500, )
    cause_text_2 = forms.CharField(required=False,max_length=500, )

    charge = forms.CharField(required=False,max_length=50,  widget=forms.Textarea(attrs={
                'style':'resize:none;'
            }), )
    charge_type_1 = forms.BooleanField(required=False,) 
    charge_type_2 = forms.BooleanField(required=False,)

    scene = forms.CharField(required=False,max_length=300,  widget=forms.Textarea(attrs={
                'style':'resize:none;'
            }), )
    # scene_date_datehalf = forms.DateField(required=False, ) 

    scene_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    scene_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(scene_date_day, scene_date_month, scene_date_year)'
    }))
    scene_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(scene_date_day, scene_date_month, scene_date_year)'
    }))

    scene_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 
    # scene_date = forms.CharField(required=False,max_length=19, ) 

    act = forms.CharField(required=False,max_length=500,  widget=forms.Textarea(attrs={
                'style':'resize:none;'
            }), )
    law = forms.CharField(required=False,max_length=200, )

    court_owner_code = forms.CharField(required=False,max_length=7, )

    prescription = forms.IntegerField(required=False, ) # อายุความ ปี

    agent_name = forms.CharField(required=False,max_length=400, )
    agent_pos = forms.CharField(required=False,max_length=400, )

    have_req_1 = forms.BooleanField(required=False,) 
    have_req_2 = forms.BooleanField(required=False,) 

    have_court_code = forms.CharField(required=False,max_length=7, ) # tb_office court_code
    have_act = forms.CharField(required=False,max_length=400, )
    have_injunc = forms.CharField(required=False,max_length=50, )

    composer_name = forms.CharField(required=False,max_length=200, )
    composer_position = forms.CharField(required=False,max_length=200, )
    writer_name = forms.CharField(required=False,max_length=200, )
    write_position = forms.CharField(required=False,max_length=200, )

    create_uid = forms.IntegerField(required=False,)
    ref_no = forms.CharField(required=False,max_length=50, widget=forms.HiddenInput(), )

    #######################

    woa_start_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    woa_start_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(woa_start_date_day, woa_start_date_month, woa_start_date_year)'
    }))
    woa_start_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(woa_start_date_day, woa_start_date_month, woa_start_date_year)'
    }))

    woa_start_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={
        'type': 'time',
        })) 

    woa_end_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    woa_end_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(woa_end_date_day, woa_end_date_month, woa_end_date_year)'
    }))
    woa_end_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(woa_end_date_day, woa_end_date_month, woa_end_date_year)'
    }))

    woa_end_date_timehalf = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'})) 


    #############################################

    #####################################################################3
    # WARRANTS AUTO-FILL SECTION
    acc_full_name = forms.CharField(required=False,max_length=250)
    acc_card_type = forms.IntegerField(required=False, )
    acc_card_id = forms.CharField(required=False,max_length=20)
    acc_age = forms.IntegerField(required=False, )

    acc_origin = forms.ChoiceField(required=False, choices=CentralForm.nation_codes.getChoices())
    acc_nation = forms.ChoiceField(required=False, choices=CentralForm.nation_codes.getChoices())

    acc_occupation = forms.CharField(required=False,max_length=100, )
    acc_addno = forms.CharField(required=False,max_length=50, )
    acc_vilno = forms.CharField(required=False,max_length=50, )
    acc_road = forms.CharField(required=False,max_length=100, )
    acc_soi = forms.CharField(required=False,max_length=100, )
    acc_near = forms.CharField(required=False,max_length=200, )
    acc_sub_district = forms.CharField(required=False,max_length=6,  widget=forms.Select(choices=CentralForm.thai_codes.getSubDistrictChoices()[:5]))
    acc_district = forms.CharField(required=False,max_length=4,  widget=forms.Select(choices=CentralForm.thai_codes.getDistrictChoices()[:5]))
    acc_province = forms.CharField(required=False,max_length=2,  widget=forms.Select(choices=CentralForm.thai_codes.getProvinceChoices()))
    acc_tel = forms.CharField(required=False,max_length=20, )