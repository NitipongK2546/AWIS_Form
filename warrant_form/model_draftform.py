from django.db import models

from django.forms.models import model_to_dict
import warrant_form.forms_central as CentralForm
from users.models import UserDataModel

from django.db.models import QuerySet


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

case_type_text = {
    1: "จ",
    2: "ยจ",
}

class AccountCardTypeChoices(models.IntegerChoices):
    THAI_ID = (1, "เลขประจำตัวประชาชน")
    PASSPORT = (2, "เลขหนังสือเดินทาง")
    NON_THAI_ID = (3, "เลขคนซึ่งไม่มีสัญชาติไทย")

class FormDraftContainer(models.Model):
    last_edit = models.DateTimeField(auto_now=True)

    form_owner = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="owned_draft")
    form_creator = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="created_draft")

    reqform_draft = "ReqformDraftDataModel"

    warrant_drafts = QuerySet["WarrantDraftDataModel"]

from django.utils import timezone

class ReqformDraftDataModel(models.Model):

    draft_container = models.OneToOneField(FormDraftContainer, on_delete=models.CASCADE, related_name="reqform_draft")

    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = (1, "ทั่วไป") # จ.
        DRUGS = (2, "ยาเสพติด") # ยจ.

    req_case_type_id = models.IntegerField(blank=True, null=True, default=ReqCaseTypeIDChoices.GENERAL) 

    court_code = models.CharField(blank=True, max_length=8)

    police_station_id = models.CharField(blank=True, max_length=8)
    req_no_plaintiff = models.CharField(blank=True, max_length=50)

    plaintiff = models.CharField(blank=True, max_length=400)
    accused = models.CharField(blank=True, max_length=400)
    
    req_title = models.CharField(blank=True, max_length=20)
    req_name = models.CharField(blank=True, max_length=300)
    req_pos = models.CharField(blank=True, max_length=400)
    req_age = models.PositiveIntegerField(blank=True, null=True, )

    req_office = models.CharField(blank=True, max_length=300)
    req_sub_district = models.CharField(blank=True, max_length=6) # tb_sub_district / sub_district_code
    req_district = models.CharField(blank=True, max_length=4)
    req_province = models.CharField(blank=True, max_length=2)

    req_tel = models.CharField(blank=True, max_length=50)

    # Start of a few unrequired field.
    # cause_type_id 
    cause_type_id = models.IntegerField(blank=True, null=True,  )
    cause_text = models.CharField(blank=True, max_length=500, )

    cause_text_piece_1 = models.CharField(blank=True, max_length=20)  # คำนำหน้า
    cause_text_piece_2 = models.CharField(blank=True, max_length=200) # ชื่อสกุล
    cause_text_piece_3 = models.CharField(blank=True, max_length=200) # ฝ่าย
    cause_text_piece_4 = models.CharField(blank=True, max_length=200) # สังกัด

    charge = models.CharField(blank=True, max_length=50, )
    charge_type_1 = models.BooleanField(default=False) 
    charge_type_2 = models.BooleanField(default=False)

    scene = models.CharField(blank=True, max_length=300, )
    # scene_date_datehalf = models.DateField(blank=True, null=True,  ) 

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

    scene_date = models.DateTimeField(blank=True, null=True,  ) 
    # scene_date = models.CharField(blank=True, null=True, max_length=19, ) 

    act = models.CharField(blank=True, max_length=500, verbose_name="มีพฤติการกระทำความผิด", )
    law = models.CharField(blank=True, max_length=200, verbose_name="ตามกฎหมาย", )

    court_owner_code = models.CharField(blank=True, max_length=8, verbose_name="ซึ่งเป็นคดีที่อยู่ในอำนาจศาล", )

    prescription = models.IntegerField(blank=True, null=True,  ) # อายุความ ปี

    agent_name = models.CharField(blank=True, max_length=400, )
    agent_pos = models.CharField(blank=True, max_length=400, )

    have_req = models.IntegerField(blank=True, null=True,  )

    have_court_code = models.CharField(blank=True, max_length=8, ) # tb_office court_code
    have_act = models.CharField(blank=True, max_length=400, )
    have_injunc = models.CharField(blank=True, max_length=50, )

    composer_name = models.CharField(blank=True, max_length=200, )
    composer_position = models.CharField(blank=True, max_length=200, )
    writer_name = models.CharField(blank=True, max_length=200, )
    write_position = models.CharField(blank=True, max_length=200, )

    create_uid = models.IntegerField(blank=True, null=True, )

    ref_no = models.CharField(blank=True, max_length=50, )

    woa_start_date = models.DateTimeField(blank=True, null=True,  )
    woa_end_date = models.DateTimeField(blank=True, null=True,  )

    #####################################################################3
    # WARRANTS AUTO-FILL SECTION
    acc_title = models.CharField(blank=True, max_length=20)
    acc_full_name = models.CharField(blank=True, max_length=250)
    acc_card_type = models.IntegerField(blank=True, null=True, choices=AccountCardTypeChoices)
    acc_card_id = models.CharField(blank=True, max_length=20)
    acc_age = models.IntegerField(blank=True, null=True,  )
    acc_origin = models.IntegerField(blank=True, null=True,  )
    acc_nation = models.IntegerField(blank=True, null=True,  )
    acc_occupation = models.CharField(blank=True, max_length=100, )
    acc_addno = models.CharField(blank=True, max_length=50, )
    acc_vilno = models.CharField(blank=True, max_length=50, )
    acc_road = models.CharField(blank=True, max_length=100, )
    acc_soi = models.CharField(blank=True, max_length=100, )
    acc_near = models.CharField(blank=True, max_length=200, )
    acc_sub_district = models.CharField(blank=True, max_length=6, )
    acc_district = models.CharField(blank=True, max_length=4, )
    acc_province = models.CharField(blank=True, max_length=2, )
    acc_tel = models.CharField(blank=True, max_length=20, )

    def __str__(self):
        return f"(ผู้ต้องสงสัย: {self.accused or '---'})"
    
    def toRealReqform(self, no_draft : bool = False) -> dict[str,]:
        
        dict_main_awis = model_to_dict(self, exclude=["id", "draft_container"])

        thai_date_now = timezone.now().astimezone(timezone.get_current_timezone())

        dict_main_awis.update({
            "req_date": thai_date_now,
            "req_year": thai_date_now.year + 543,
        })

        if not no_draft:
            dict_main_awis.update({
                "draft_id": self
            })

        if self.cause_type_id == 1:
            assembled_text = self.cause_text_piece_2
            dict_main_awis.update({f"cause_text": assembled_text})

        elif self.cause_type_id == 2:
            assembled_text = self.cause_text_piece_1 + self.cause_text_piece_2

            dict_main_awis.update({f"cause_text": assembled_text})
        return dict_main_awis
    
    def getAccusedInfo(self) -> dict[str]:
        return {
            "charge_type_1": self.charge_type_1,
            "charge_type_2": self.charge_type_2,
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
        }
    
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
            dict_main_awis.update({f"have_req_1": 1})
        else:
            dict_main_awis.update({f"have_req_2": 1})

        return dict_main_awis

WOA_TYPE_CHOICES = [
    (1, "47"),
    (2, "47 ทวิ"),
]

woa_type_dict = {
    1: "47",
    2: "47 ทวิ"
}

# หมายเรียกที่ติดไปด้วย
class WarrantDraftDataModel(models.Model):
    class AppointmentTypeChoices(models.IntegerChoices):
        PRESCRIPTION = (1, "กำหนดอายุความ")
        APPOINTMENT = (2, "กำหนดนัด")

    draft_container = models.ForeignKey(FormDraftContainer, on_delete=models.CASCADE, related_name="warrant_drafts")

    woa_type = models.IntegerField(blank=True, null=True, default=2)
    woa_date = models.DateTimeField(blank=True, null=True)

    fault_type_id = models.IntegerField(blank=True, null=True, default=2) #(อาญา.แพ่ง)
    send_to_name = models.CharField(max_length=250, blank=True) # ส่งหมายถึงใคร
    cause_text = models.CharField(max_length=400, blank=True) # ด้วย

    charge = models.CharField(max_length=250, blank=True)
    charge_type_1 = models.BooleanField(default=False) 
    charge_type_2 = models.BooleanField(default=False)
    charge_type_2_1 = models.BooleanField(default=False)
    charge_type_2_2 = models.BooleanField(default=False)
    charge_type_2_3 = models.BooleanField(default=False)
    charge_type_3 = models.BooleanField(default=False)
    charge_other_text = models.CharField(max_length=250, blank=True)

    acc_full_name = models.CharField(max_length=250, blank=True)
    acc_card_type = models.IntegerField(choices=AccountCardTypeChoices, blank=True, null=True)
    acc_card_id = models.CharField(max_length=20, blank=True,)
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
    appointment_date = models.DateTimeField(blank=True, null=True)

    woa_refno = models.CharField(max_length=16, blank=True)
    plaintiff = models.CharField(max_length=400, blank=True)
    court_name = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"(หมายจับ: {self.acc_full_name})"
    
    def toRealWarrant(self) -> dict[str,]:
        
        dict_main_awis = model_to_dict(self, exclude=["id", "draft_container"])

        thai_date_now = timezone.now().astimezone(timezone.get_current_timezone())

        dict_main_awis.update({
            "woa_date": thai_date_now,
        })

        return dict_main_awis