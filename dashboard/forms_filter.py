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

    # (99, "ยกเลิกคำร้อง"),           # Cancel during Form Await
]

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

class DashboardFilterForm(forms.Form):
    req_no_plaintiff = forms.ChoiceField(
        choices=get_req_no_plaintiff_choices,
        required=False,
    )
    accused = forms.ChoiceField(
        choices=get_accused_choices,
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
    req_no_plaintiff = forms.ChoiceField(
        choices=get_req_no_plaintiff_choices,
        required=False,
    )
    accused = forms.ChoiceField(
        choices=get_accused_choices,
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