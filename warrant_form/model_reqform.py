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

class ReqformDataModel(models.Model):
    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = (1, "ทั่วไป") # จ.
        DRUGS = (2, "ยาเสพติด") # ยจ.
    
    req_form_number = models.IntegerField(blank=True, null=True)
    
    req_date = models.DateTimeField(blank=True, null=True)
    req_year = models.PositiveIntegerField()

    req_case_type_id = models.IntegerField(choices=ReqCaseTypeIDChoices) 

    court_code = models.CharField(max_length=8, choices=CentralForm.court_codes.getChoices())

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
            return f"{case_type_text.get(self.req_case_type_id)}.{self.req_form_number}/{self.req_year + 543}"
        
        return "-"
    
    # def getReqno(self):
    #     if self.reqno:
    #         return self.reqno
        
    #     case_type_text = {
    #         1: "จ.",
    #         2: "ยจ.",
    #     }
    #     buddhist_year = self.req_year + 543
    #     reqno = f"{case_type_text.get(self.req_case_type_id)}{self.req_form_number}/{buddhist_year}"

    #     self.reqno = reqno

    #     return reqno


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
        def datetime_format(datetime_obj : datetime.datetime):
            if datetime_obj:
                return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            
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
    

    def convertBacktoFormView(self) -> dict[str,]:
        dict_main_awis = model_to_dict(self)

        duped_list = ["accused", "plaintiff", "court_name"]
        time_split_list = ["woa_start_date", "woa_end_date", "scene_date"]

        dict_main_awis = CentralForm.createDupe(duped_list, dict_main_awis)
        dict_main_awis = CentralForm.splitTime(time_split_list, dict_main_awis)


        dict_main_awis.update({
            "court_name_1": CentralForm.court_codes.getValueOf(self.court_code),
            "court_name_2": CentralForm.court_codes.getValueOf(self.court_code)
        })

        if self.cause_type_id:
            dict_main_awis.update({f"cause_type_id_{self.cause_type_id}": 1})
            dict_main_awis.update({f"cause_text_{self.cause_type_id}": self.cause_text})

        if self.have_req:
            dict_main_awis.update({f"have_req_1": 1})
        else:
            dict_main_awis.update({f"have_req_2": 1})

        return dict_main_awis
    
    def prepareTextToSpeech(self):
        prepared_text = \
        "ทดสอบ"
# f"""
# คำร้องขอออกหมายจับที่ {self.req_form_number}\n
# วันที่ {self.req_day} เดือน {THAI_MONTHS.get(self.req_month)} ปี พ.ศ. {self.req_year + 543}\n
# ผู้ร้อง: {self.plaintiff},

# ข้าพเจ้า {self.req_name},
# ตำแหน่ง {self.req_pos},
# อายุ {self.req_age} ปี,
# อาชีพ พนักงานของรัฐ,
# สถานที่ทำงาน {self.req_office},
# จังหวัด {CentralForm.thai_codes.getValueOfCode(self.req_province)},
# {"อำเภอ" if int(self.req_province) != 10 else "เขต"} {CentralForm.thai_codes.getValueOfCode(self.req_district)},
# {"ตำบล" if int(self.req_province) != 10 else "แขวง"} {CentralForm.thai_codes.getValueOfCode(self.req_sub_district)},
# โทรศัพท์ {self.req_tel},

# ขอยื่นคำร้องขอออกหมายจับยื่นต่อศาล,
# ดังมีข้อความที่จะกล่าวดังต่อไปนี้,

# ข้อ 1. 
# ด้วย {assemble_cause(self.cause_type_id, self.cause_text)}

# ว่า {self.acc_full_name},
# เลขบัตรประชาชน {self.acc_card_id},

# อายุ {self.acc_age},
# เชื้อชาติ {CentralForm.nation_codes.getValueOf(self.acc_origin)},
# สัญชาติ {CentralForm.nation_codes.getValueOf(self.acc_nation)},
# อาชีพ {self.acc_occupation},

# อยู่บ้านเลขที่ {self.acc_addno},
# หมู่ที่ {self.acc_vilno},
# ถนน {self.acc_road},

# ตรอก ซอย {self.acc_soi},
# ใกล้เคียง {self.acc_near},
# จังหวัด {CentralForm.thai_codes.getValueOfCode(self.acc_province)},
# {"อำเภอ" if self.acc_province and int(self.acc_province) != 10 else "เขต"} {CentralForm.thai_codes.getValueOfCode(self.acc_district)},
# {"ตำบล" if self.acc_province and int(self.acc_province) != 10 else "แขวง"} {CentralForm.thai_codes.getValueOfCode(self.acc_sub_district)},

# โทรศัพท์ {self.acc_tel}

# {"ได้หรือน่าจะได้กระทำความผิดอาญาร้ายแรงซึ่งมีอัตราโทษจำคุกอย่างสูงเกิน3ปี" if self.charge_type_1 else ""}

# {"ได้หรือน่าจะได้กระทำความผิดอาญา, และน่าจะหลบหนี, หรือจะไปยุ่งเหยิงกับพยานหลักฐาน, หรือก่ออันตรายประการอื่น" if self.charge_type_2 else ""}

# เหตุเกิดที่ {self.scene}

# เมื่อวันที่ {self.scene_date.day} เดือน {THAI_MONTHS.get(self.scene_date.month)} พ.ศ. {self.scene_date.year + 543} เวลา {self.scene_date.time()} น.

# มีพฤติการณ์กระทำความผิดที่เกี่ยวกับเหตุออกหมายจับ คือ {self.act},
# เป็นการกระทำความผิดฐาน {self.charge},
# ตามกฎหมาย {self.law},
# รายละเอียดข้อมูลและพยานหลักฐาน ปรากฎตามที่เอกสารที่แนบมาพร้อมนี้

# ข้อ 2.,
# ผู้ร้องประสงค์จะทำการจับกุม{self.accused}

# จึงขอให้ศาลออกหมายจับ 
# {self.accused} มาดำเนินคดี

# นับตั้งแต่วันที่ 
# {self.woa_start_date.day},
# {THAI_MONTHS.get(self.woa_start_date.month)},
# {self.woa_start_date.year + 543},
# {self.woa_start_date.time()} น.,
# แต่ไม่เกิน 
# {self.woa_end_date.day},
# {THAI_MONTHS.get(self.woa_end_date.month)},
# {self.woa_end_date.year + 543},
# {self.woa_end_date.time()} น.,
# ในการยื่นคำร้องนี้ ผู้ร้องได้มอบหมายให้ {self.agent_name},
# ตำแหน่ง {self.agent_pos},

# ซึ่งเป็นผู้ใต้บังคับบัญชา, เป็นผู้นำคำร้องมายื่นต่อศาล
# และหากศาลเรียกสอบถามเมื่อใด, ผู้ร้องพร้อมจะมาให้ศาลสอบในทันที

# ผู้ร้อง {"เคย" if self.have_req else "ไม่เคย"} ร้องขอให้ศาล {self.have_court_code} ออกหมายจับบุคคลดังกล่าว 

# {
# f"""
# โดยอาศัยเหตุแห่งการร้องขอเดียวกันนี้ หรือเหตุอื่น (ระบุ)
# {self.have_act}
# และศาลสั่ง 
# {self.have_injunc}
# """

# if self.have_req else ""
# }

# ควรมิควรแล้วแต่จะโปรด.
# {self.req_name}.
# ผู้ร้อง
# """

        return prepared_text
        
def assemble_cause(cause_id : int, cause_text : str):
    temp = {
        1: f"{cause_text} มาแจ้งความร้องทุกข์ต่อพนักงานสอบสวน",
        2: f"ปรากฎจากการสืบสวน/สอบสวนของ {cause_text}"
    }

    return temp.get(cause_id, "")