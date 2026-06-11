from django import forms
from warrant_form.model_reqform import ReqformDataModel

from dashboard.models import VisualReqformData, FormAwaitingApproval
from dashboard.warrant_wrapper import VisualWarrantData

status_choices = [
    (00, "-----"),              # 

    (1, "ร่างคำร้อง"),              # 

    (10, "กำลังรอการพิจารณา"),         # Form Await
    (11, "ไม่ผ่านการพิจารณา"),      # Form Await
    # (12, "ผ่านการพิจารณา"),        # Form Await
    (20, "รอศาลตอบรับ"),          # Visual Form
    # (21, "รับ"),                  # Visual Form
    (22, "ไม่รับ"),                # Visual Form
    (23, "รอรายงานผลหมายจับ"),    # Visual Form (Accepted)
    (24, "จับไม่สำเร็จ"),            # Visual Form (Failed)
    (25, "รายงานผลสำเร็จ"),        # Visual Form (All Warrant Success)

    (99, "ยกเลิกคำร้อง"),           # Cancel during Form Await
]

def get_req_year_choices():
    choices = set()
    for reqform in ReqformDataModel.objects.all():
        if reqform.req_year == "-":
            continue
        choices.add(
            (reqform.req_year, reqform.req_year)
        )

    return [("", "-----")] + list(choices)

def get_reqno_choices():
    choices = set()
    for reqform in ReqformDataModel.objects.all():
        if reqform.getReqno() == "-":
            continue
        choices.add(
            (reqform.getReqno(), reqform.getReqno())
        )

    return [("", "-----")] + list(choices)

def get_req_no_plaintiff_choices():
    choices = set()
    for reqform in ReqformDataModel.objects.all():
        if not reqform.req_no_plaintiff:
            continue
        choices.add(
            (reqform.req_no_plaintiff, reqform.req_no_plaintiff)
        )

    return [("", "-----")] + list(choices)

def get_accused_choices():
    choices = set()
    for reqform in ReqformDataModel.objects.all():
        if not reqform.accused:
            continue
        choices.add(
            (reqform.accused, reqform.accused)
        )

    return [("", "-----")] + list(choices)

def get_req_name_choices():
    choices = set()
    for reqform in ReqformDataModel.objects.all():
        if not reqform.req_name:
            continue
        choices.add(
            (reqform.req_name, reqform.req_name)
        )

    return [("", "-----")] + list(choices)

class DashboardFilterForm(forms.Form):
    req_no_plaintiff = forms.CharField(
        max_length=200,
        required=False,
    )
    req_name = forms.CharField(
        max_length=200,
        required=False,
    )
    accused = forms.CharField(
        max_length=200,
        required=False,
    )

    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "datetimepicker"}
        ),
        required=False,
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "datetimepicker"}
        ),
        required=False,
    )

    status = forms.ChoiceField(
        choices=status_choices,
        required=False,
    )

stats_status_choices = [
    (00, "-----"),              # 

    (10, "กำลังรอการพิจารณา"),         # Form Await
    (11, "ไม่ผ่านการพิจารณา"),      # Form Await
    # (12, "ผ่านการพิจารณา"),        # Form Await
    (20, "รอศาลตอบรับ"),          # Visual Form
    # (21, "รับ"),                  # Visual Form
    (22, "ไม่รับ"),                # Visual Form
    (23, "รอรายงานผลหมายจับ"),    # Visual Form (Accepted)
    (24, "จับไม่สำเร็จ"),            # Visual Form (Failed)
    (25, "รายงานผลสำเร็จ"),        # Visual Form (All Warrant Success)

    (99, "ยกเลิกคำร้อง"),           # Cancel during Form Await
]

class StatisticFilterForm(forms.Form):
    req_year = forms.ChoiceField(
        choices=get_req_year_choices,
        required=False,
    )
    reqno = forms.ChoiceField(
        choices=get_reqno_choices,
        required=False,
    )

    req_no_plaintiff = forms.CharField(
        max_length=200,
        required=False,
    )
    req_name = forms.CharField(
        max_length=200,
        required=False,
    )
    accused = forms.CharField(
        max_length=200,
        required=False,
    )

    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "datetimepicker"}
        ),
        required=False,
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "datetimepicker"}
        ),
        required=False,
    )

    status = forms.ChoiceField(
        choices=stats_status_choices,
        required=False,
    )