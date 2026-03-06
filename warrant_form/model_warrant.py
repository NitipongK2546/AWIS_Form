from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

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

    woa_date_day = models.PositiveIntegerField(blank=True, null=True)
    woa_date_month = models.PositiveIntegerField(blank=True, null=True)
    woa_date_year = models.PositiveIntegerField(blank=True, null=True)
    woa_date_timehalf = models.TimeField(blank=True, null=True)

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

    woa_no = models.IntegerField()
    woa_refno = models.CharField(max_length=16, blank=True)
    woa_type = models.IntegerField()

    def toAPICompatibleDict(self, prefix : str = None) -> dict[str, object]:
        """
        Convert the model object into a dictionary that fits what the API required.
        It uses model_to_dict to, first, convert the model into a dictionary with matching field names,
        then convert or remove some fields to match the API.\n
        It is, of course, not JSON object, so don't forget to json.dumps(dict) it later.
        """
        dict_warrant = toAPICompatibleDictGeneral(self)

        date_list = ["appointment_date", ]

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
    
##########################################################################