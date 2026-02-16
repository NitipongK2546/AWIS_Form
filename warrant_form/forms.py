from django import forms
from django.db import models
from warrant_form.models import WarrantDataModel
from django.forms.models import model_to_dict
import datetime

class SpecialAWISDataFormModelPartOne(models.Model):
    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = 1, "ทั่วไป(จ)"
        DRUGS = 2, "ยาเสพติด(ยจ)"

    class CauseTypeIDChoices(models.IntegerChoices):
        PROBLEM_REPORT = 1, "ร้องทุกข์"
        INTERROGATION = 2, "สืบสวนสอบสวน"

    court_code = models.CharField(max_length=7, verbose_name="รหัส")

    req_year = models.IntegerField()
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
    cause_type_id = models.IntegerField(choices=CauseTypeIDChoices, blank=True, null=True)
    cause_text = models.CharField(max_length=500, verbose_name="ฐานความผิด", blank=True)
    charge = models.CharField(max_length=50, blank=True)
    charge_type_1 = models.BooleanField() 
    charge_type_2 = models.BooleanField()

    scene = models.CharField(max_length=300, blank=True)
    scene_date_datehalf = models.DateField(blank=True, null=True) 
    scene_date_timehalf = models.TimeField(blank=True, null=True) 
    scene_date = models.CharField(max_length=19, blank=True) 

    act = models.CharField(max_length=500, verbose_name="มีพฤติการกระทำความผิด", blank=True)
    law = models.CharField(max_length=200, verbose_name="ตามกฎหมาย", blank=True)

    court_owner_code = models.CharField(max_length=7, verbose_name="ซึ่งเป็นคดีที่อยู่ในอำนาจศาล", blank=True)

    prescription = models.IntegerField(blank=True, null=True) # อายุความ ปี

    agent_name = models.CharField(max_length=400, blank=True)
    agent_pos = models.CharField(max_length=400, blank=True)

    have_req = models.BooleanField() 
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
    acc_occupation = models.CharField(max_length=100)
    acc_addno = models.CharField(max_length=50)
    acc_vilno = models.CharField(max_length=50)
    acc_road = models.CharField(max_length=100)
    acc_soi = models.CharField(max_length=100)
    acc_near = models.CharField(max_length=200)
    acc_sub_district = models.CharField(max_length=6)
    acc_district = models.CharField(max_length=4)
    acc_province = models.CharField(max_length=2)
    acc_tel = models.CharField(max_length=20)

    def toAPICompatibleDict(self) -> dict[str, object]:
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

        DATEHALF_STR = "scene_date_datehalf"
        TIMEHALF_STR = "scene_date_timehalf"

        buddhist_date_half = dict_main_awis.get(DATEHALF_STR)
        time_half = dict_main_awis.get(TIMEHALF_STR)

        if buddhist_date_half and time_half:
            # First, we have to convert Year: B.E. to A.D.
            BUDDHIST_ERA_YEAR_DIFF = 543
            one_year = datetime.timedelta(days=365)
            buddhist_era_difference_datetime = BUDDHIST_ERA_YEAR_DIFF * one_year

            iso_date_half = buddhist_date_half - buddhist_era_difference_datetime

            # Leave a space between date and time.
            full_datetime = f"{iso_date_half} {time_half}"
            dict_main_awis.update({"scene_date": full_datetime})

            dict_main_awis.pop(DATEHALF_STR)
            dict_main_awis.pop(TIMEHALF_STR)

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
            dict_main_awis.pop(key)

        return dict_main_awis

class MainAWISForm(forms.ModelForm):
    class Meta:
        model = SpecialAWISDataFormModelPartOne
        exclude = ["scene_date", "scene_date_datehalf", "scene_date_timehalf"]
        # fields = "__all__"
        # widgets = {
        #     'scene_date_datehalf': forms.DateInput(attrs={'type': 'date'}),
        #     'scene_date_timehalf': forms.TimeInput(attrs={'type': 'time'}),
        # }

class WarrantForm(forms.ModelForm):
    class Meta:
        model = WarrantDataModel
        fields = "__all__"
        widgets = {
            "woa_date": forms.DateInput(attrs={'type': 'date'}),
        }