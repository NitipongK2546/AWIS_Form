from django import forms
from django.core.exceptions import ValidationError

from _log_utils import file_logger as FileLogger
from _log_utils.file_logger import AccessType

from django.utils import timezone

from users.models import UserDataModel
import warrant_form.forms_central as CentralForm

from warrant_form.model_reqform import ReqformDataModel

class CourtUserCreationForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(render_value=False, attrs={
        'autocomplete': 'off',
        'class': 'password-field'
    }))
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(render_value=False, attrs={
        'autocomplete': 'off',
        'class': 'password-field'
    }))

class LogQuery(forms.Form):
    def getReqnoChoices():
        try:
            all_forms = ReqformDataModel.objects.all()

            return [("", "ไม่เลือก")] + [(form.reqno, form.reqno) for form in all_forms]
        except:
            return [("", "ไม่เลือก")]
        
    def getUserChocies():
        try:
            all_users = UserDataModel.objects.all()

            return [("", "ไม่เลือก")] + [(user.api_uid, f"({user.username}, id:{user.api_uid})") for user in all_users]
        except:
            return [("", "ไม่เลือก")]

    action_choices = AccessType.choices
    
    timelogged_trigger = forms.BooleanField(required=False)
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


    user_trigger = forms.BooleanField(required=False)
    user_id = forms.ChoiceField(choices=getUserChocies(), required=False)
    
    action_trigger = forms.BooleanField(required=False)
    action = forms.MultipleChoiceField(choices=action_choices, required=False,
                                       widget=forms.CheckboxSelectMultiple())

    reqno_trigger = forms.BooleanField(required=False)
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
        