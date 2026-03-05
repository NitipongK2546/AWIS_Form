from django.db import models
from django.forms.models import model_to_dict
import datetime
# from django.core import serializers

# Create your models here.

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

# หมายเรียกที่ติดไปด้วย
class WarrantDataModel(models.Model):
    """
    หมายเรียกที่ติดให้กับแบบฟอร์ม
    1 แบบฟอร์มสามารถใช้ได้หลายตัว
    """
    class AppointmentTypeChoices(models.IntegerChoices):
        PRESCRIPTION = 1, "กำหนดอายุความ"
        APPOINTMENT = 2, "กำหนดนัด"

    class AccountCardTypeChoices(models.IntegerChoices):
        THAI_ID = 1, "เลขประจำตัวประชาชน"
        PASSPORT = 2, "เลขหนังสือเดินทาง"
        NON_THAI_ID = 3, "เลขคนซึ่งไม่มีสัญชาติไทย"

    woa_date = models.CharField(max_length=19, blank=True, null=True)

    fault_type_id = models.IntegerField() # UNCLEAR, HOW IS IT A NUMBER? ความ (อาญา.แพ่ง)
    send_to_name = models.CharField(max_length=250) # ส่งหมายถึงใคร
    cause_text = models.CharField(max_length=400) # ด้วย

    charge = models.CharField(max_length=250)
    charge_type_1 = models.BooleanField() 
    charge_type_2 = models.BooleanField()
    charge_type_2_1 = models.BooleanField()
    charge_type_2_2 = models.BooleanField()
    charge_type_2_3 = models.BooleanField()
    charge_type_3 = models.BooleanField()
    charge_other_text = models.CharField(max_length=250, blank=True)

    acc_full_name = models.CharField(max_length=250)
    acc_card_type = models.IntegerField(choices=AccountCardTypeChoices)
    acc_card_id = models.CharField(max_length=20)
    acc_origin = models.IntegerField(blank=True, null=True) # This gotta be choices, again.
    acc_nation = models.IntegerField(blank=True, null=True) # Except no choices in descriptions.
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

    appointment_type = models.IntegerField(choices=AppointmentTypeChoices, blank=True, null=True)
    appointment_date = models.CharField(max_length=19, blank=True, null=True) # SAME DATE FORMAT AS BELOW

    woa_refno = models.CharField(max_length=10, blank=True)
    woa_type = models.IntegerField()

    def toAPICompatibleDict(self, prefix : str = None) -> dict[str, object]:
        """
        Convert the model object into a dictionary that fits what the API required.
        It uses model_to_dict to, first, convert the model into a dictionary with matching field names,
        then convert or remove some fields to match the API.\n
        It is, of course, not JSON object, so don't forget to json.dumps(dict) it later.
        """
        dict_warrant = toAPICompatibleDictGeneral(self)

        date_list = ["appointment_date", "woa_date"]

        for date in date_list:
            date_value = dict_warrant.get(date)
            if (not date_value) or len(date_value) != 19:
                dict_warrant.update({
                    date: "1970-01-01 12:00:00",
                })

        prefixed_dict = {}
        if prefix:
            prefixed_dict = {f"{prefix}-{key}":value for key, value in dict_warrant.items()}

            return prefixed_dict

        return dict_warrant

# ข้อมูลหลัก ๆ ส่งให้กับ API
class MainAWISDataModel(models.Model):
    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = 1, "ทั่วไป(จ)"
        DRUGS = 2, "ยาเสพติด(ยจ)"

    class CauseTypeIDChoices(models.IntegerChoices):
        PROBLEM_REPORT = 1, "ร้องทุกข์"
        INTERROGATION = 2, "สืบสวนสอบสวน"

    court_code = models.CharField(max_length=7, verbose_name="รหัส")

    req_year = models.IntegerField()
    req_case_type_id = models.IntegerField(choices=ReqCaseTypeIDChoices) # CHOICES

    # The API specification wants 5, but the real thing is 8, so ehhhhh.
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
    cause_type_id = models.IntegerField(choices=CauseTypeIDChoices, blank=True, null=True)
    cause_text = models.CharField(max_length=500, verbose_name="ฐานความผิด", blank=True)
    charge = models.CharField(max_length=50, blank=True)
    charge_type_1 = models.BooleanField() 
    charge_type_2 = models.BooleanField()

    scene = models.CharField(max_length=300, blank=True)
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
    write_position = models.CharField(max_length=200, blank=True)
    #############################################

    create_uid = models.IntegerField() # USER ที่สร้างข้อมูล
    ref_no = models.CharField(max_length=50, blank=True)

    woa_start_date = models.CharField(max_length=19, blank=True, null=True) # THIS TIME, IT"S DATE, WITHOUT THE TIME
    woa_end_date = models.CharField(max_length=19, blank=True, null=True) # MAYBE TIMEFIELD INSTEAD OF DATEFIELD??

    # def clean(self):
    #     self.scene_date = " ".join(self.scene_date)

    #     return super().clean()

    # คิดว่าหมาย 
    # ManyToMany อยู่ในนี้เพราะถ้ามีการแก้ไขก็คิดว่าต้องแก้ใน AWIS Form 
    warrants = models.ManyToManyField(WarrantDataModel)

    def toAPICompatibleDict(self, prefix : str = None) -> dict[str, object]:
        """
        Convert the model object into a dictionary that fits what the API required.
        It uses model_to_dict to, first, convert the model into a dictionary with matching field names,
        then convert or remove some fields to match the API.\n
        It is, of course, not JSON object, so don't forget to json.dumps(dict) it later.
        """
        dict_main_awis = toAPICompatibleDictGeneral(self)

        date_list = ["scene_date", "woa_start_date", "woa_end_date"]

        for date in date_list:
            date_value = dict_main_awis.get(date)
            if (not date_value) or len(date_value) != 19:
                dict_main_awis.update({
                    date: "1970-01-01 12:00:00",
                })

        prefixed_dict = {}
        if prefix:
            prefixed_dict = {f"{prefix}-{key}":value for key, value in dict_main_awis.items()}

            return prefixed_dict

        return dict_main_awis

    
    def toAPICompatibleDictWithConvertedWarrants(self, prefix : str = None) -> dict[str, object]:
        cleaned_dict = self.toAPICompatibleDict(prefix)

        warrants_obj = self.warrants.all()
        warrants_list = [item.toAPICompatibleDict() for item in warrants_obj]

        if prefix:
            cleaned_dict.update({f"{prefix}_warrants": warrants_list})
            return cleaned_dict
        
        cleaned_dict.update({f"warrants": warrants_list})
        return cleaned_dict
        
        
