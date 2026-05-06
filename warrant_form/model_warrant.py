from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
# from warrant_form.model_reqform import ReqformDataModel

import warrant_form.forms_central as CentralForm

import json

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

WOA_TYPE_CHOICES = [
    (1, "47"),
    (2, "47 ทวิ"),
]

FAULT_TYPE_ID_CHOICES = [
    (1, "แพ่ง"),
    (2, "อาญา"),
]

from django.utils import timezone
import datetime

# หมายเรียกที่ติดไปด้วย
class WarrantDataModel(models.Model):
    """
    หมายเรียกที่ติดให้กับแบบฟอร์ม
    1 แบบฟอร์มสามารถใช้ได้หลายตัว
    """
    class AppointmentTypeChoices(models.IntegerChoices):
        PRESCRIPTION = (1, "กำหนดอายุความ")
        APPOINTMENT = (2, "กำหนดนัด")

    class AccountCardTypeChoices(models.IntegerChoices):
        THAI_ID = (1, "เลขประจำตัวประชาชน")
        PASSPORT = (2, "เลขหนังสือเดินทาง")
        NON_THAI_ID = (3, "เลขคนซึ่งไม่มีสัญชาติไทย")

    # reqforms

    reqforms = "ReqformDataModel"

    woa_no = models.IntegerField(blank=True, null=True)
    woa_refno = models.CharField(max_length=16, blank=True, unique=True)
    woa_type = models.IntegerField()

    woa_year = models.PositiveIntegerField(blank=True, null=True)
    # For my sanity, I'm seperating year and date. It won't be confusing, I swear. 
    woa_date = models.DateTimeField(blank=True, null=True)
    # woa_start_date = models.DateTimeField(blank=True, null=True)
    # woa_end_date = models.DateTimeField(blank=True, null=True)
    # Start and end date is used for display

    fault_type_id = models.IntegerField() # (อาญา.แพ่ง)
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
    acc_card_type = models.IntegerField(choices=AccountCardTypeChoices, blank=True, null=True)
    acc_card_id = models.CharField(max_length=20)
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

    appointment_type = models.IntegerField(choices=AppointmentTypeChoices, blank=True, null=True)
    # appointment_date = models.CharField(max_length=19, blank=True, null=True) # SAME DATE FORMAT AS BELOW

    appointment_date = models.DateTimeField(blank=True, null=True)

    plaintiff = models.CharField(max_length=400, blank=True)
    court_name = models.CharField(max_length=250, blank=True)
    # judge_name = models.CharField(max_length=250, blank=True)

    def __str__(self):
        # return json.dumps({
        #     "type": ["warrant_form", "WarrantDataModel"],
        #     "id": self.pk,
        #     "woa_no": self.woa_no
        # }, ensure_ascii=False)
        return f"(pk: {self.pk}, woa_no: {self.woa_no})"
    
    def getLogInfoDict(self):
        return {
            "type": ["warrant_form", "WarrantDataModel"],
            "id": self.pk,
            "woa_no": self.woa_no
        }

    def get_woa_type_text(self) -> str:
        woa_type_dict = dict(WOA_TYPE_CHOICES)

        return woa_type_dict.get(self.woa_type, "-----")
    
    def get_fault_type_text(self) -> str:
        fault_type_dict = dict(FAULT_TYPE_ID_CHOICES)

        return fault_type_dict.get(self.fault_type_id, "-----")
    
    def get_woa_no_and_year(self) -> str:
        return f"{self.woa_no if self.woa_no else '000'}/{self.woa_year if self.woa_year else '0000'}"

    def toAPICompatibleDict(self, prefix : str = None) -> dict[str, object]:
        def datetime_format(datetime_obj : datetime.datetime):
            if datetime_obj:
                return datetime_obj.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S")
            
            return timezone.datetime.fromtimestamp(0, timezone.UTC).strftime("%Y-%m-%d %H:%M:%S")

        result_dict = {
            "woa_refno": self.woa_refno,
            "woa_date": datetime_format(self.woa_date),
            "fault_type_id": self.fault_type_id,
            "send_to_name": self.send_to_name,
            "cause_text": self.cause_text,
            "charge": self.charge,
            "charge_type_1": 1 if self.charge_type_1 else 0,
            "charge_type_2": 1 if self.charge_type_2 else 0,
            "charge_type_2_1": 1 if self.charge_type_2_1 else 0,
            "charge_type_2_2": 1 if self.charge_type_2_2 else 0,
            "charge_type_2_3": 1 if self.charge_type_2_3 else 0,
            "charge_type_3": 1 if self.charge_type_3 else 0,
            "charge_other_text": self.charge_other_text,
            "acc_full_name": self.acc_full_name,
            "acc_card_type": self.acc_card_type,
            "acc_card_id": self.acc_card_id,
            "acc_origin": self.acc_origin,
            "acc_nation": self.acc_nation,
            "acc_occupation": self.acc_occupation,
            "acc_addno": self.acc_addno,
            "acc_vilno": self.acc_vilno,
            "acc_road": self.acc_road,
            "acc_soi": self.acc_soi,
            "acc_near": self.acc_near,
            "acc_sub_district": self.acc_sub_district,
            "acc_district": self.acc_district,
            "acc_province": self.acc_province,
            "acc_tel": self.acc_tel,
            "appointment_type": self.appointment_type,
            "appointment_date": datetime_format(self.appointment_date),
            "woa_type": self.woa_type
        }

        return result_dict
    
    def convertBacktoFormView(self) -> dict[str, object]:
        dict_main_awis = model_to_dict(self)

        duped_list = ["acc_full_name", ]
        time_split_list = ["woa_date", "appointment_date"]

        dict_main_awis.update({
            "woa_no": "12345/2569",
            "court_name": self.reqforms.first().getCourtName(),
            "judge_name": self.reqforms.first().judge_name,
            "plaintiff": self.reqforms.first().plaintiff,
            "prescription": self.reqforms.first().prescription,
            "woa_start_date": self.reqforms.first().woa_start_date,
            "woa_end_date": self.reqforms.first().woa_end_date,
        })

        dict_main_awis = CentralForm.splitTime(time_split_list, dict_main_awis)

        for item in duped_list:
            dict_main_awis.update({f"{item}_1" : dict_main_awis.get(item)})
            dict_main_awis.update({f"{item}_2" : dict_main_awis.get(item)})

        return dict_main_awis
    
##########################################################################

def cleanDateTimeFields(current_dict : dict):

    included_fields = ["woa_date", "appointment_date"]

    for field in included_fields:
        current_dict = reattachDateTime(current_dict, field)
    
    return current_dict

def reattachDateTime(current_dict : dict, field : str):
    
    scene_date_year = current_dict.get(f"{field}_year")
    scene_date_month = current_dict.get(f"{field}_month")
    scene_date_day = current_dict.get(f"{field}_day")
    scene_date_timehalf = current_dict.get(f"{field}_timehalf")
    combined_date = ""
    combined_datetime = "1970-01-01 00:00:00"
    # combined_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
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