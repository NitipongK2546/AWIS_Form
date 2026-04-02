from django.db import models
# from warrant_form.forms import SpecialAWISDataFormModelPartOne
from warrant_form.model_reqform import ReqformDataModel

from users.models import UserDataModel
from zoneinfo import ZoneInfo
import json

# Create your models here.

class FormAwaitingApproval(models.Model):
    """
    เก็บฟอร์มและข้อมูลต่าง ๆ ของฟอร์มเพื่อรอการอนุมัติ
    """

    class Meta:
        default_permissions = ()
        # permissions = [
        #     ("approve_formawaitingapproval", ""),
        # ]

    class ApprovalStatus(models.IntegerChoices):
        REJECTED = (0, "ไม่ผ่านการอนุมติ")
        PENDING = (1, "กำลังรอพิจารณา")
        APPROVED = (2, "ผ่านการอนุมัติ")
    
    form = models.OneToOneField(ReqformDataModel, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(blank=True, null=True)

    form_creator = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="created_visual_form")
    form_owner = models.ForeignKey(UserDataModel, on_delete=models.PROTECT, related_name="owned_visual_form")

    approve_status = models.IntegerField(choices=ApprovalStatus)

    def __str__(self):
        # return json.dumps({
        #     "type": ["dashboard", "FormAwaitingApproval"],
        #     "id": self.pk,
        #     "form": self.form
        # }, ensure_ascii=False, default=str)
        return f"<FormAwaitApproval (pk: {self.pk}, reqform: {self.form})>"
    
    def getLogInfoDict(self):
        return {
            "type": ["dashboard", "FormAwaitingApproval"],
            "id": self.pk,
            "form": self.form.getLogInfoDict()
        }
    
    # def getDataAsTable(self):

    
    def toAPICompatibleDict(self) -> dict[str, object]:
        return self.form.toAPICompatibleDictWithConvertedWarrants()

class VisualReqformData(models.Model):
    """
    เก็บข้อมูลฟอร์มที่ได้ทำการส่งไปแล้ว และสามารถให้บุคคลภายนอกเชื่อม API เข้ามาแก้ไขข้อมูลสถานะได้
    """
    class Meta:
        default_permissions = ()
        # permissions = [
        #     ("approve_visualreqformdata", ""),
        # ]

    class AcceptStatus(models.IntegerChoices):
        DENIED = (0, "ไม่รับ")
        ACCEPTED = (1, "รับ")
        WAITING = (99, "รอการพิจารณา")
    
    form = models.OneToOneField(ReqformDataModel, on_delete=models.CASCADE, related_name='finalized_form')

    # THIS NAME IS CORRECT, DON'T CHANGE THIS, FUTURE READER!!!
    recive_date = models.DateTimeField(blank=True, null=True)
    accept_date = models.DateTimeField(blank=True, null=True)

    accept = models.IntegerField(choices=AcceptStatus, blank=True, null=True)

    def __str__(self):
        # return json.dumps({
        #     "type": ["warrant_form", "VisualReqformData"],
        #     "id": self.pk,
        #     "form": self.form
        # }, ensure_ascii=False)
        
        return f"<Approved Form (pk: {self.pk}, reqform: {self.form})>"
    
    def toAPICompatibleDict(self) -> dict[str, object]:
        return self.form.toAPICompatibleDictWithConvertedWarrants()
    
    def getReqNoPlaintiff(self):
        form : ReqformDataModel = self.form

        return form.req_no_plaintiff
    
    def getReqNo(self):
        form : ReqformDataModel = self.form

        return form.reqno
    
    def getLogInfoDict(self):
        return {
            "type": ["warrant_form", "VisualReqformData"],
            "id": self.pk,
            "form": self.form.getLogInfoDict()
        }
    