from django import forms
from django.core.exceptions import ValidationError

from _log_utils import file_logger as FileLogger
from _log_utils.file_logger import AccessType

from django.utils import timezone

from users.models import UserDataModel
import warrant_form.forms_central as CentralForm

# from users.models import PermissionList, PermissionType, PathPermission

# from awis_custom_settings.settings import PermissionChoices

# class PermissionAddForm(forms.Form):
#     view = forms.BooleanField(required=False)
#     edit = forms.BooleanField(required=False)
#     create = forms.BooleanField(required=False)
#     delete = forms.BooleanField(required=False)
#     approve = forms.BooleanField(required=False)
#     perm = forms.ChoiceField(choices=PermissionChoices)

#     selected_type = forms.ChoiceField(choices=PathPermission.get_all_keys())

from warrant_form.model_reqform import ReqformDataModel

class LogQuery(forms.Form):
    def getReqnoChoices():
        all_forms = ReqformDataModel.objects.all()

        return [("", "-"*6)] + [(form.reqno, form.reqno) for form in all_forms]
    
    def getUserChocies():
        all_users = UserDataModel.objects.all()

        return [("", "-"*6)] + [(user.api_uid, f"({user.username}, id:{user.api_uid})") for user in all_users]

    action_choices = [("", "-"*6)] + AccessType.choices
    

    start_day = forms.IntegerField(widget=forms.Select(choices=CentralForm.day_choices))
    start_month = forms.IntegerField(widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }))
    start_year = forms.IntegerField(widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }))

    end_day = forms.IntegerField(widget=forms.Select(choices=CentralForm.day_choices))
    end_month = forms.IntegerField(widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }))
    end_year = forms.IntegerField(widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(req_day, req_month, req_year)'
    }))


    # user_id = forms.IntegerField(required=False)
    # reqno = forms.CharField(max_length=20, required=False,)

    user_id = forms.ChoiceField(choices=getUserChocies(), required=False)
    action = forms.ChoiceField(choices=action_choices, required=False)
    reqno = forms.ChoiceField(choices=getReqnoChoices(), required=False)

    # def clean(self):
    #     def cleanDate(data : dict):
    #         try:
    #             start_obj = timezone.datetime(
    #                 data.get("start_year"), data.get("start_month"), data.get("start_day"), tzinfo=timezone.get_current_timezone()
    #             )
    #             end_obj = timezone.datetime(
    #                 data.get("end_year"),  data.get("end_month"), data.get("end_day"),
    #                 tzinfo=timezone.get_current_timezone()
    #             )
    #             if start_obj > end_obj:
    #                 raise ValidationError("Start Date is after the End Date")
    #         except Exception as e:
    #             print(e)
        
    #     data = self.cleaned_data
            
    #     cleanDate(data)
        