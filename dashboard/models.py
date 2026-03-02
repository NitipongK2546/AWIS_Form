from django.db import models
# from warrant_form.forms import SpecialAWISDataFormModelPartOne
from warrant_form.models import MainAWISDataModel

from users.models import UserDataModel
from zoneinfo import ZoneInfo

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
    
    form = models.OneToOneField(MainAWISDataModel, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(blank=True, null=True)

    form_creator = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="created_form")
    form_owner = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="owned_form")

    approve_status = models.IntegerField(choices=ApprovalStatus)

    def __str__(self):
        converted_date = self.date_created.astimezone(ZoneInfo("Asia/Bangkok")).strftime("%d %B %Y, %H:%M")
        finalized_date = f"{converted_date} น."
        
        return f"ID: {self.id} | {self.get_approve_status_display()} | {self.form_creator} | {finalized_date}"