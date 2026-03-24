from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
import datetime
from warrant_form import forms_central as CentralForm

from warrant_form.model_warrant import WarrantDataModel

class ReqformDataModel(models.Model):
    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = (1, "ทั่วไป") # จ.
        DRUGS = (2, "ยาเสพติด") # ยจ.
    
    reqno = models.CharField(max_length=50, blank=True, unique=True)
    # เป็นการผสมกันระหว่าง case_type_id, req_form_number, และ req_year

    req_form_number = models.IntegerField()
    
    req_day = models.PositiveIntegerField()
    req_month = models.PositiveIntegerField()
    req_year = models.PositiveIntegerField()

    req_case_type_id = models.IntegerField(choices=ReqCaseTypeIDChoices) 

    court_name = models.CharField(max_length=250, blank=True)
    court_code = models.CharField(max_length=7, verbose_name="รหัส")

    judge_name = models.CharField(max_length=250, blank=True)

    police_station_id = models.CharField(max_length=8) #REFER id -> tb_police_station
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
    cause_type_id = models.IntegerField(blank=True, null=True)
    cause_text = models.CharField(max_length=500, blank=True)

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

    scene_date = models.DateTimeField(blank=True, null=True) 
    # scene_date = models.CharField(max_length=19, blank=True) 

    act = models.CharField(max_length=500, verbose_name="มีพฤติการกระทำความผิด", blank=True)
    law = models.CharField(max_length=200, verbose_name="ตามกฎหมาย", blank=True)

    court_owner_code = models.CharField(max_length=7, verbose_name="ซึ่งเป็นคดีที่อยู่ในอำนาจศาล", blank=True)

    prescription = models.IntegerField(blank=True, null=True) # อายุความ ปี

    agent_name = models.CharField(max_length=400, blank=True)
    agent_pos = models.CharField(max_length=400, blank=True)

    have_req = models.IntegerField(blank=True, null=True)

    have_court_code = models.CharField(max_length=7, blank=True) # tb_office court_code
    have_act = models.CharField(max_length=400, blank=True)
    have_injunc = models.CharField(max_length=50, blank=True)

    composer_name = models.CharField(max_length=200, blank=True)
    composer_position = models.CharField(max_length=200, blank=True)
    writer_name = models.CharField(max_length=200, blank=True)
    write_position = models.CharField(max_length=200, blank=True)

    create_uid = models.IntegerField()

    ref_no = models.CharField(max_length=50, blank=True)

    woa_start_date = models.DateTimeField(blank=True, null=True)
    woa_end_date = models.DateTimeField(blank=True, null=True)

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

    warrants = models.ManyToManyField(WarrantDataModel, related_name="reqforms")


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

        included_fields = ["scene_date", "woa_start_date", "woa_end_date"]

        dict_main_awis = model_to_dict(self)

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

        for field in included_fields:
            datetime_obj : datetime.datetime = dict_main_awis.get(field)
            dict_main_awis.update({
                field: datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            })

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

        current_dict.pop("req_day")
        current_dict.pop("req_month")

        current_dict.update({"req_year": current_dict.get("req_year") + 543})

        current_dict.pop("court_name")

        current_dict.pop("acc_full_name")

        current_dict.pop("acc_origin")
        current_dict.pop("acc_nation")
        current_dict.pop("acc_occupation")

        current_dict.pop("acc_card_id")
        current_dict.pop("acc_card_type")

        current_dict.pop("acc_sub_district")
        current_dict.pop("acc_district")
        current_dict.pop("acc_province")

        current_dict.pop("acc_addno")
        current_dict.pop("acc_vilno")
        current_dict.pop("acc_road")
        current_dict.pop("acc_soi")
        current_dict.pop("acc_near")
        current_dict.pop("acc_tel")

        return current_dict
    
    
    def toAPICompatibleDictWithConvertedWarrants(self, prefix : str = None) -> dict[str, object]:
        cleaned_dict = self.toAPICompatibleDict()

        warrants_obj = self.warrants.all()
        warrants_list = [item.toAPICompatibleDict() for item in warrants_obj]

        if prefix:
            cleaned_dict.update({f"{prefix}_warrants": warrants_list})
            return cleaned_dict
        
        cleaned_dict.update({f"warrants": warrants_list})

        cleaned_dict.pop("reqno")
        cleaned_dict.pop("req_form_number")

        return cleaned_dict
    

    def convertBacktoFormView(self) -> dict[str,]:
        dict_main_awis = model_to_dict(self)

        duped_list = ["accused", "plaintiff", "court_name"]
        time_split_list = ["woa_start_date", "woa_end_date", "scene_date"]

        dict_main_awis = CentralForm.createDupe(duped_list, dict_main_awis)
        dict_main_awis = CentralForm.splitTime(time_split_list, dict_main_awis)

        if self.cause_type_id:
            dict_main_awis.update({f"cause_type_id_{self.cause_type_id}": 1})
            dict_main_awis.update({f"cause_text_{self.cause_type_id}": self.cause_text})

        if self.have_req:
            dict_main_awis.update({f"have_req_{self.have_req + 1}": 1})

        return dict_main_awis
    
    def prepareTextToSpeech(self):
        prepared_text = ""

        return prepared_text
