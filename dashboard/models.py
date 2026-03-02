from django.db import models
from warrant_form.forms import SpecialAWISDataFormModelPartOne

from users.models import UserDataModel

# Create your models here.

class FormApprovalDataContainer(models.Model):
    """
    เก็บฟอร์มและข้อมูลต่าง ๆ ของฟอร์มเพื่อรอการอนุมัติ
    """

    class Meta:
        permissions = [
            ("can_approve_form", "Can approve form"),
        ]

    class ApprovalStatus(models.IntegerChoices):
        REJECTED = (0, "ไม่ผ่านการอนุมติ")
        PENDING = (1, "กำลังรอพิจารณา")
        APPROVED = (2, "ผ่านการอนุมัติ")
    
    form = models.OneToOneField(SpecialAWISDataFormModelPartOne, on_delete=models.CASCADE)

    date_created = models.DateTimeField()
    date_approved = models.DateTimeField(blank=True, null=True)

    form_creator = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="created_form")
    form_owner = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="owned_form")

    approve_status = models.IntegerField(choices=ApprovalStatus)

    def __str__(self):
        return f"{self.approve_status} | {self.form_creator} | {self.date_created}"