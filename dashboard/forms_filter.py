from django import forms
from warrant_form.model_reqform import ReqformDataModel

status_choices = [
    ("", "-----"),
    (0, "ร่างคำร้อง"),
    (1, "รอการพิจารณา"),
    (2, "ไม่ผ่านการพิจารณา"),
    (3, "ผ่านการพิจารณา"),
    (4, "รอศาลตอบรับ"),
    (5, "รับ"),
    (6, "ไม่รับ"),
    (7, "รอรายงานผลหมายจับ"),
    (8, "จับไม่สำเร็จ"),
    (9, "รายงานผลสำเจ็จ"),
]

def get_reqno_choices():
    choices = [
        ("", "-----")
    ]
    for reqform in ReqformDataModel.objects.all():
        if reqform.getReqno() == "-":
            continue
        choices.append(
            (reqform.getReqno(), reqform.getReqno())
        )

    return choices

def get_req_no_plaintiff_choices():
    choices = [
        ("", "-----")
    ]
    for reqform in ReqformDataModel.objects.all():
        if not reqform.req_no_plaintiff:
            continue
        choices.append(
            (reqform.req_no_plaintiff, reqform.req_no_plaintiff)
        )

    return choices

def get_accused_choices():
    choices = [
        ("", "-----")
    ]
    for reqform in ReqformDataModel.objects.all():
        if not reqform.accused:
            continue
        choices.append(
            (reqform.accused, reqform.accused)
        )

    return choices

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