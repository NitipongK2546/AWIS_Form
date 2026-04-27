from django.db import models

from warrant_form.model_warrant import WarrantDataModel
from django.forms.models import model_to_dict
import warrant_form.forms_central as CentralForm
from users.models import UserDataModel

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

class ReqformDraftDataModel(models.Model):

    class ReqCaseTypeIDChoices(models.IntegerChoices):
        GENERAL = (1, "ทั่วไป") # จ.
        DRUGS = (2, "ยาเสพติด") # ยจ.
    
    reqno = models.CharField(blank=True, null=True, max_length=50,  unique=True)
    # เป็นการผสมกันระหว่าง case_type_id, req_form_number, และ req_year

    req_form_number = models.IntegerField(blank=True, null=True, )
    
    req_day = models.PositiveIntegerField(blank=True, null=True, )
    req_month = models.PositiveIntegerField(blank=True, null=True, )
    req_year = models.PositiveIntegerField(blank=True, null=True, )

    req_case_type_id = models.IntegerField(blank=True, null=True, choices=ReqCaseTypeIDChoices) 

    court_name = models.CharField(blank=True, null=True, max_length=250, )
    court_code = models.CharField(blank=True, null=True, max_length=7, verbose_name="รหัสศาล")

    judge_name = models.CharField(blank=True, null=True, max_length=250, )

    police_station_id = models.CharField(blank=True, null=True, max_length=8)
    req_no_plaintiff = models.CharField(blank=True, null=True, max_length=50)

    plaintiff = models.CharField(blank=True, null=True, max_length=400)
    accused = models.CharField(blank=True, null=True, max_length=400)
    
    req_name = models.CharField(blank=True, null=True, max_length=300)
    req_pos = models.CharField(blank=True, null=True, max_length=400)
    req_age = models.PositiveIntegerField(blank=True, null=True, )

    req_office = models.CharField(blank=True, null=True, max_length=300)
    req_sub_district = models.CharField(blank=True, null=True, max_length=6) # tb_sub_district / sub_district_code
    req_district = models.CharField(blank=True, null=True, max_length=4)
    req_province = models.CharField(blank=True, null=True, max_length=2)

    req_tel = models.CharField(blank=True, null=True, max_length=50)

    # Start of a few unrequired field.
    # cause_type_id 
    cause_type_id = models.IntegerField(blank=True, null=True,  )
    cause_text = models.CharField(blank=True, null=True, max_length=500, )

    charge = models.CharField(blank=True, null=True, max_length=50, )
    charge_type_1 = models.BooleanField(default=False) 
    charge_type_2 = models.BooleanField(default=False)

    scene = models.CharField(blank=True, null=True, max_length=300, )
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

    act = models.CharField(blank=True, null=True, max_length=500, verbose_name="มีพฤติการกระทำความผิด", )
    law = models.CharField(blank=True, null=True, max_length=200, verbose_name="ตามกฎหมาย", )

    court_owner_code = models.CharField(blank=True, null=True, max_length=7, verbose_name="ซึ่งเป็นคดีที่อยู่ในอำนาจศาล", )

    prescription = models.IntegerField(blank=True, null=True,  ) # อายุความ ปี

    agent_name = models.CharField(blank=True, null=True, max_length=400, )
    agent_pos = models.CharField(blank=True, null=True, max_length=400, )

    have_req = models.IntegerField(blank=True, null=True,  )

    have_court_code = models.CharField(blank=True, null=True, max_length=7, ) # tb_office court_code
    have_act = models.CharField(blank=True, null=True, max_length=400, )
    have_injunc = models.CharField(blank=True, null=True, max_length=50, )

    composer_name = models.CharField(blank=True, null=True, max_length=200, )
    composer_position = models.CharField(blank=True, null=True, max_length=200, )
    writer_name = models.CharField(blank=True, null=True, max_length=200, )
    write_position = models.CharField(blank=True, null=True, max_length=200, )

    create_uid = models.IntegerField(blank=True, null=True, )

    ref_no = models.CharField(blank=True, null=True, max_length=50, )

    woa_start_date = models.DateTimeField(blank=True, null=True,  )
    woa_end_date = models.DateTimeField(blank=True, null=True,  )

    #####################################################################3
    # WARRANTS AUTO-FILL SECTION
    acc_full_name = models.CharField(blank=True, null=True, max_length=250)
    acc_card_type = models.IntegerField(blank=True, null=True,  )
    acc_card_id = models.CharField(blank=True, null=True, max_length=20)
    acc_age = models.IntegerField(blank=True, null=True,  )
    acc_origin = models.IntegerField(blank=True, null=True,  )
    acc_nation = models.IntegerField(blank=True, null=True,  )
    acc_occupation = models.CharField(blank=True, null=True, max_length=100, )
    acc_addno = models.CharField(blank=True, null=True, max_length=50, )
    acc_vilno = models.CharField(blank=True, null=True, max_length=50, )
    acc_road = models.CharField(blank=True, null=True, max_length=100, )
    acc_soi = models.CharField(blank=True, null=True, max_length=100, )
    acc_near = models.CharField(blank=True, null=True, max_length=200, )
    acc_sub_district = models.CharField(blank=True, null=True, max_length=6, )
    acc_district = models.CharField(blank=True, null=True, max_length=4, )
    acc_province = models.CharField(blank=True, null=True, max_length=2, )
    acc_tel = models.CharField(blank=True, null=True, max_length=20, )

    # warrants = models.ManyToManyField(WarrantDataModel, blank=True, null=True,related_name="reqforms")

    def __str__(self):

        return f"(pk: {self.pk}, reqno: {self.reqno})"
    
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
    

class FormDraftContainer(models.Model):
    form_owner = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="owned_draft")
    form_creator = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="created_draft")

    reqform = models.OneToOneField(ReqformDraftDataModel, on_delete=models.CASCADE)

    warrants = list["WarrantDraftDataModel"]

WOA_TYPE_CHOICES = [
    (1, "47"),
    (2, "47 ทวิ"),
]

# หมายเรียกที่ติดไปด้วย
class WarrantDraftDataModel(models.Model):
    class AppointmentTypeChoices(models.IntegerChoices):
        PRESCRIPTION = (1, "กำหนดอายุความ")
        APPOINTMENT = (2, "กำหนดนัด")

    class AccountCardTypeChoices(models.IntegerChoices):
        THAI_ID = (1, "เลขประจำตัวประชาชน")
        PASSPORT = (2, "เลขหนังสือเดินทาง")
        NON_THAI_ID = (3, "เลขคนซึ่งไม่มีสัญชาติไทย")

    # reqforms

    woa_date = models.DateTimeField(blank=True, null=True)

    fault_type_id = models.IntegerField(blank=True, null=True) #(อาญา.แพ่ง)
    send_to_name = models.CharField(max_length=250, blank=True) # ส่งหมายถึงใคร
    cause_text = models.CharField(max_length=400, blank=True) # ด้วย

    charge = models.CharField(max_length=250, blank=True)
    charge_type_1 = models.BooleanField() 
    charge_type_2 = models.BooleanField()
    charge_type_2_1 = models.BooleanField()
    charge_type_2_2 = models.BooleanField()
    charge_type_2_3 = models.BooleanField()
    charge_type_3 = models.BooleanField()
    charge_other_text = models.CharField(max_length=250, blank=True)

    acc_full_name = models.CharField(max_length=250, blank=True)
    acc_card_type = models.IntegerField(choices=AccountCardTypeChoices, blank=True, null=True)
    acc_card_id = models.CharField(max_length=20, blank=True)
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

    woa_no = models.IntegerField(blank=True, null=True)
    woa_refno = models.CharField(max_length=16, blank=True)

    woa_type = models.IntegerField()

    plaintiff = models.CharField(max_length=400, blank=True)
    court_name = models.CharField(max_length=250, blank=True)