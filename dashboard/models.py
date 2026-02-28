from django.db import models
from warrant_form.forms import SpecialAWISDataFormModelPartOne

# Create your models here.

class FormApprovalDataContainer(models.Model):
    """
    เก็บฟอร์มและข้อมูลต่าง ๆ ของฟอร์มเพื่อรอการอนุมัติ
    """

    class ApprovalStatus(models.IntegerChoices):
        REJECTED = (0, "ไม่ผ่านการอนุมติ")
        PENDING = (1, "กำลังรอพิจารณา")
        APPROVED = (2, "ผ่านการอนุมัติ")
    
    form = models.OneToOneField(SpecialAWISDataFormModelPartOne, on_delete=models.CASCADE)

    date_created = models.DateTimeField()
    date_approved = models.DateTimeField(blank=True, null=True)

    # form_creator = models.ForeignKey(on_delete=models.PROTECT)
    # form_owner = models.ForeignKey(on_delete=models.PROTECT)

    approve_status = models.IntegerField(choices=ApprovalStatus)