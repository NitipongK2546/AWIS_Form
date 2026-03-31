from django.db import models
# from warrant_form.forms import SpecialAWISDataFormModelPartOne
from warrant_form.model_reqform import ReqformDataModel
from warrant_form.model_warrant import WarrantDataModel

from users.models import UserDataModel
from zoneinfo import ZoneInfo

class VisualWarrantData(models.Model):
    """
    เก็บข้อมูลฟอร์มที่ได้ทำการส่งไปแล้ว และสามารถให้บุคคลภายนอกเชื่อม API เข้ามาแก้ไขข้อมูลสถานะได้
    """
    class Meta:
        default_permissions = ()
        # permissions = [
        #     ("approve_visualwarrantdata", ""),
        # ]

    class AcceptStatus(models.IntegerChoices):
        DENIED = (0, "ไม่อนุมัติ")
        ACCEPTED = (1, "อนุมัติ")
        WAITING = (99, "รอการพิจารณา")
    
    warrant = models.OneToOneField(WarrantDataModel, on_delete=models.CASCADE, related_name='finalized_warrant')

    # THIS NAME IS CORRECT, DON'T CHANGE THIS, FUTURE READER!!!

    judge_name = models.CharField(max_length=250)
    court_injunction = models.IntegerField(choices=AcceptStatus, blank=True, null=True)
    injunction_date = models.DateTimeField(blank=True, null=True)

    file_path = models.CharField(max_length=250, blank=True,)
    because = models.CharField(max_length=300, blank=True,)

    def __str__(self):
        return f"<Warrant Data (pk: {self.pk}, {self.warrant})>"