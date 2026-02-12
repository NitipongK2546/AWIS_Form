from django.db import models
from django.core import serializers

# Create your models here.

class ArrayWarrantDataModel(models.Model):
    woa_date = models.CharField(max_length=10)

    fault_type_id = models.IntegerField() # UNCLEAR, HOW IS IT A NUMBER? ความ (อาญา.แพ่ง)
    send_to_name = models.CharField(max_length=250) # ส่งหมายถึงใคร
    cause_text = models.CharField(max_length=400) # ด้วย

    charge = models.CharField(max_length=250)
    charge_type_1 = models.IntegerField() #CHOICES
    charge_type_2 = models.IntegerField()
    charge_type_2_1 = models.IntegerField()
    charge_type_2_2 = models.IntegerField()
    charge_type_2_3 = models.IntegerField()
    charge_type_3 = models.IntegerField()
    charge_other_text = models.CharField(max_length=250)

    acc_full_name = models.CharField(max_length=250)
    acc_card_type = models.IntegerField()
    acc_card_id = models.CharField(max_length=20)
    acc_origin = models.IntegerField()
    acc_nation = models.IntegerField()
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

    appointment_type = models.IntegerField()
    appointment_date = models.CharField(max_length=19) # SAME DATE FORMAT AS BELOW

    woa_start_date = models.CharField(max_length=10) # THIS TIME, IT"S DATE, WITHOUT THE TIME
    woa_end_date = models.CharField(max_length=10) # MAYBE TIMEFIELD INSTEAD OF DATEFIELD??
    woa_refno = models.CharField(max_length=10)

# Please choose a better name next time, thank you.
class MainJSONWarrantDataModel(models.Model):
    court_code = models.CharField(max_length=7)

    req_year = models.IntegerField()
    req_year_type_id = models.IntegerField() # CHOICES

    police_station_id = models.CharField(max_length=5) #REFER id -> tb_police_station
    req_no_plaintiff = models.CharField(max_length=50)

    plaintiff = models.CharField(max_length=400)
    accused = models.CharField(max_length=400)
    req_name = models.CharField(max_length=300)
    req_pos = models.CharField(max_length=400)
    req_age = models.IntegerField()

    req_office = models.CharField(max_length=300)
    req_sub_district = models.CharField(max_length=6) # tb_sub_district / sub_district_code
    req_district = models.CharField(max_length=4)
    req_province = models.CharField(max_length=2)

    req_tel = models.CharField(max_length=50)

    cause_type_id = models.IntegerField()
    cause_text = models.CharField(max_length=500)
    charge = models.CharField(max_length=50)
    charge_type_1 = models.IntegerField() # Models. INTEGERCHOICES
    charge_type_2 = models.IntegerField()

    scene = models.CharField(max_length=300)
    scene_date = models.CharField(max_length=19) ## MODELS.DATETIMEFIELD FORMAT -> "YYYY-MM-DD HH24:MI:SS" or "2019-01-01 20:00:00" 19 letters
    act = models.CharField(max_length=500)
    law = models.CharField(max_length=200)

    court_owner_code = models.CharField(max_length=7)

    prescription = models.IntegerField() # อายุความ ปี

    agent_name = models.CharField(max_length=400)
    agent_pos = models.CharField(max_length=400)

    have_req = models.IntegerField() # CHOICE AGAIN WHY IS IT NOT BOOLEAN
    have_court_code = models.CharField(max_length=7) # tb_office court_code
    have_act = models.CharField(max_length=400)
    have_injunc = models.CharField(max_length=50)

    composer_name = models.CharField(max_length=200)
    composer_position = models.CharField(max_length=200)
    writer_name = models.CharField(max_length=200)

    #############################################
    # THE FILE SAID "write_position" BUT IS IT "write" or "writer"?
    #
    write_position = models.CharField(max_length=200)
    #############################################

    create_uid = models.IntegerField() # USER ที่สร้างข้อมูล
    ref_no = models.CharField(max_length=50)
    warrants = models.OneToOneField(ArrayWarrantDataModel, on_delete=models.CASCADE)