from django import forms
from _log_utils import file_logger as FileLogger
from _log_utils.file_logger import AccessType

from django.utils import timezone

from users.models import UserDataModel

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
    

    start_date = forms.DateField(
        required=False
    )
    end_date = forms.DateField(
        required=False
    )

    # user_id = forms.IntegerField(required=False)
    # reqno = forms.CharField(max_length=20, required=False,)

    user_id = forms.ChoiceField(choices=getUserChocies(), required=False)
    action = forms.ChoiceField(choices=action_choices, required=False)
    reqno = forms.ChoiceField(choices=getReqnoChoices(), required=False)
