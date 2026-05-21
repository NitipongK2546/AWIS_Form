from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
import datetime
from warrant_form import forms_central as CentralForm

import json

from warrant_form.model_warrant import WarrantDataModel

# THAI_MONTHS = {
#     1: ("ม.ค.", "มกราคม"),
#     2: ("ก.พ.", "กุมภาพันธ์"),
#     3: ("มี.ค.", "มีนาคม"),
#     4: ("เม.ย.", "เมษายน"),
#     5: ("พ.ค.", "พฤษภาคม"),
#     6: ("มิ.ย.", "มิถุนายน"),
#     7: ("ก.ค.", "กรกฎาคม"),
#     8: ("ส.ค.", "สิงหาคม"),
#     9: ("ก.ย.", "กันยายน"),
#     10:("ต.ค.", "ตุลาคม"),
#     11:("พ.ย.", "พฤศจิกายน"),
#     12:("ธ.ค.", "มกราคม"),
# }

case_type_text = {
    1: "จ",
    2: "ยจ",
}

req_case_type_id_text = {
    1: "ทั่วไป",
    2: "ยาเสพติด"
}

THAI_MONTHS = {
    1: "มกราคม",
    2: "กุมภาพันธ์",
    3: "มีนาคม",
    4: "เมษายน",
    5: "พฤษภาคม",
    6: "มิถุนายน",
    7: "กรกฎาคม",
    8: "สิงหาคม",
    9: "กันยายน",
    10:"ตุลาคม",
    11:"พฤศจิกายน",
    12:"มกราคม",
}

from .model_draftform import ReqformDraftDataModel

class ReqformDataModel(models.Model):
    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = (1, "ทั่วไป") # จ.
        DRUGS = (2, "ยาเสพติด") # ยจ.

    # New field added specially because people didn't tell me how it's supposed to be made.
    # Oh well.
    draft_id = models.ForeignKey(ReqformDraftDataModel, on_delete=models.PROTECT)
    last_update_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    req_form_number = models.IntegerField(blank=True, null=True)
    
    req_date = models.DateTimeField(blank=True, null=True)
    req_year = models.PositiveIntegerField()

    req_case_type_id = models.IntegerField(choices=ReqCaseTypeIDChoices) 

    court_code = models.CharField(max_length=8)

    judge_name = models.CharField(max_length=250, blank=True)

    police_station_id = models.CharField(max_length=8) #REFER id -> tb_police_station
    req_no_plaintiff = models.CharField(max_length=50, unique=True)

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

    court_owner_code = models.CharField(max_length=8, verbose_name="ซึ่งเป็นคดีที่อยู่ในอำนาจศาล", blank=True)

    prescription = models.IntegerField(blank=True, null=True) # อายุความ ปี

    agent_name = models.CharField(max_length=400, blank=True)
    agent_pos = models.CharField(max_length=400, blank=True)

    have_req = models.IntegerField(blank=True, null=True)

    have_court_code = models.CharField(max_length=8, blank=True) # tb_office court_code
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

    def __str__(self):
        # return json.dumps({
        #     "type": ["warrant_form", "ReqformDataModel"],
        #     "id": self.pk,
        #     "reqno": self.reqno
        # }, ensure_ascii=False)
        return f"(pk: {self.pk}, req_no_plaintiff: {self.req_no_plaintiff})"
    
    def getLogInfoDict(self):
        return {
            "type": ["warrant_form", "ReqformDataModel"],
            "id": self.pk,
            "reqno": self.getReqno()
        }
    
    def getCourtName(self) -> str:
        return CentralForm.court_codes.getValueOf(self.court_code)
    
    def getReqno(self):
        if self.req_form_number:
            return f"{case_type_text.get(self.req_case_type_id)}.{self.req_form_number}/{self.req_year}"
        
        return "-"

    def getReqCaseTypeIDText(self, data_type = "abbr"):
        """
        type = abbr ตัวย่อ\n
        type = full ตัวเต็ม
        """
        if data_type == "abbr":
            return case_type_text.get(data_type)

        return req_case_type_id_text.get(data_type)
    
    def toAPICompatibleDict(self,) -> dict[str, object]:
        def datetime_format(datetime_obj : datetime.datetime):
            if datetime_obj:
                return datetime_obj.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S")
            
            return timezone.datetime.fromtimestamp(0, timezone.UTC).strftime("%Y-%m-%d %H:%M:%S")

        result_dict = {
            "court_code": self.court_code,
            "req_year": self.req_year,
            "req_case_type_id": self.req_case_type_id,
            "police_station_id": self.police_station_id,
            "req_no_plaintiff": self.req_no_plaintiff,
            "plaintiff": self.plaintiff,
            "accused": self.accused,
            "req_name": self.req_name,
            "req_pos": self.req_pos,
            "req_age": self.req_age,
            "req_office": self.req_office,
            "req_sub_district": self.req_sub_district,
            "req_district": self.req_district,
            "req_province": self.req_province,
            "req_tel": self.req_tel,
            "cause_type_id": self.cause_type_id,
            "cause_text": self.cause_text,
            "charge": self.charge,
            "charge_type_1": 1 if self.charge_type_1 else 0,
            "charge_type_2": 1 if self.charge_type_2 else 0,
            "scene": self.scene,
            "scene_date": datetime_format(self.scene_date),
            "act": self.act,
            "law": self.law,
            "court_owner_code": self.court_owner_code,
            "prescription": self.prescription,
            "woa_start_date": datetime_format(self.woa_start_date),
            "woa_end_date": datetime_format(self.woa_end_date),
            "agent_name": self.agent_name,
            "agent_pos": self.agent_pos,
            "have_req": self.have_req,
            "have_court_code": self.have_court_code,
            "have_act": self.have_act,
            "have_injunc": self.have_injunc,
            "composer_name": self.composer_name,
            "composer_position": self.composer_position,
            "writer_name": self.writer_name,
            "write_position": self.write_position,
            "create_uid": self.create_uid,
            "ref_no": self.ref_no,
        }
        warrant_list = []
        for warrant in self.warrants.all():
            warrant_dict = warrant.toAPICompatibleDict()
            warrant_list.append(warrant_dict)

        result_dict.update({
            "warrants": warrant_list
        })

        return result_dict
    

    def convertBacktoFormView(self, month_as_text : bool = False, two_digit_year : bool = False, buddhist_year : bool = False) -> dict[str,]:
        dict_main_awis = model_to_dict(self)

        duped_list = ["accused",]
        time_split_list = ["woa_start_date", "woa_end_date", "scene_date", "req_date"]

        dict_main_awis = CentralForm.createDupe(duped_list, dict_main_awis)
        dict_main_awis = CentralForm.splitTime(time_split_list, dict_main_awis, month_as_text=month_as_text, buddhist_year=buddhist_year)

        dict_main_awis.update({
            "court_name_1": CentralForm.court_codes.getValueOf(self.court_code),
            "court_name_2": CentralForm.court_codes.getValueOf(self.court_code)
        })

        if self.cause_type_id:
            dict_main_awis.update({f"cause_type_id_{self.cause_type_id}": 1})
            dict_main_awis.update({f"cause_text_{self.cause_type_id}": self.cause_text})

        if self.req_year:
            dict_main_awis.update({
                "req_year": str(self.req_year)[-2:]
            })

        if self.have_req:
            dict_main_awis.update({f"have_req_1": True})
        else:
            dict_main_awis.update({f"have_req_2": True})

        return dict_main_awis
    
    def convertToDocumentData(self):
        data_dict = self.convertBacktoFormView(month_as_text=True, two_digit_year=True, buddhist_year=True)

        data_dict.update({f"cause_type_id_{self.cause_type_id}": True})

        return data_dict

def assemble_cause(cause_id : int, cause_text : str):
    temp = {
        1: f"{cause_text} มาแจ้งความร้องทุกข์ต่อพนักงานสอบสวน",
        2: f"ปรากฎจากการสืบสวน/สอบสวนของ {cause_text}"
    }

    return temp.get(cause_id, "")