from django.db import models
from django.forms.models import model_to_dict
# from django.core import serializers

# Create your models here.

# หมายเรียกที่ติดให้กับแบบฟอร์ม
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

    woa_date = models.DateField(max_length=10, blank=True)

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
    appointment_date = models.DateTimeField(max_length=19, blank=True, null=True) # SAME DATE FORMAT AS BELOW

    woa_start_date = models.DateField(max_length=10, blank=True, null=True) # THIS TIME, IT"S DATE, WITHOUT THE TIME
    woa_end_date = models.DateField(max_length=10, blank=True, null=True) # MAYBE TIMEFIELD INSTEAD OF DATEFIELD??
    woa_refno = models.CharField(max_length=10, blank=True)

# class WarrantDataModelNew(models.Model):
#     """
#     อันนี้เป็น Object เพื่อรองรับข้อมูลจากการค้นหา Warrant ผ่าน API
#     """
    
#     woa_date = models.CharField(max_length=10)

#     fault_type_id = models.IntegerField() # UNCLEAR, HOW IS IT A NUMBER? ความ (อาญา.แพ่ง)
#     send_to_name = models.CharField(max_length=250) # ส่งหมายถึงใคร
#     cause_text = models.CharField(max_length=400) # ด้วย

#     charge = models.CharField(max_length=250)
#     charge_type_1 = models.IntegerField() #CHOICES
#     charge_type_2 = models.IntegerField()
#     charge_type_2_1 = models.IntegerField()
#     charge_type_2_2 = models.IntegerField()
#     charge_type_2_3 = models.IntegerField()
#     charge_type_3 = models.IntegerField()
#     charge_other_text = models.CharField(max_length=250)

#     # acc -> stands for accused.
#     acc_full_name = models.CharField(max_length=250)
#     acc_card_type = models.IntegerField()
#     acc_card_id = models.CharField(max_length=20)
#     acc_origin = models.IntegerField()
#     acc_nation = models.IntegerField()
#     acc_occupation = models.CharField(max_length=100)
#     acc_addno = models.CharField(max_length=50)
#     acc_vilno = models.CharField(max_length=50)
#     acc_road = models.CharField(max_length=100)
#     acc_soi = models.CharField(max_length=100)
#     acc_near = models.CharField(max_length=200)
#     acc_sub_district = models.CharField(max_length=6)
#     acc_district = models.CharField(max_length=4)
#     acc_province = models.CharField(max_length=2)
#     acc_tel = models.CharField(max_length=20)

#     appointment_type = models.IntegerField()
#     appointment_date = models.CharField(max_length=19) # SAME DATE FORMAT AS BELOW

#     woa_start_date = models.CharField(max_length=10) # THIS TIME, IT"S DATE, WITHOUT THE TIME
#     woa_end_date = models.CharField(max_length=10) # MAYBE TIMEFIELD INSTEAD OF DATEFIELD??
#     woa_refno = models.CharField(max_length=10)

#     ## ADDITIONAL VARIABLE FOR WARRANT STATUS SEARH
#     # status = models.CharField(max_length=8) # CHOICES -> Active/Inactive
#     # court_code = models.CharField(max_length=7)
#     # woa_type = models.IntegerField() # CHOICES AGAIN
#     # woa_year = models.IntegerField()
#     # woa_no = models.IntegerField()

#     # req_num_case_type_id = models.IntegerField() # CHOICES
#     # police_station_id = models.CharField(max_length=5)

#     # black_case_num_prefix = models.IntegerField() 
#     # black_case_num = models.IntegerField() 
#     # black_case_num_year = models.IntegerField() 
#     # red_case_num_prefix = models.IntegerField() 
#     # red_case_num = models.IntegerField() 
#     # red_case_num_year = models.IntegerField() 

# แบบฟอร์ม
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
    cause_type_id = models.IntegerField(choices=CauseTypeIDChoices)
    cause_text = models.CharField(max_length=500, verbose_name="ฐานความผิด", blank=True)
    charge = models.CharField(max_length=50, blank=True)
    charge_type_1 = models.BooleanField() 
    charge_type_2 = models.BooleanField()

    scene = models.CharField(max_length=300, blank=True)
    scene_date = models.DateTimeField(blank=True, null=True) ## MODELS.DATETIMEFIELD FORMAT -> "YYYY-MM-DD HH24:MI:SS" or "2019-01-01 20:00:00" 19 letters
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

    # คิดว่าหมาย 
    # ManyToMany อยู่ในนี้เพราะถ้ามีการแก้ไขก็คิดว่าต้องแก้ใน AWIS Form 
    # warrants = models.ManyToManyField(WarrantDataModel)