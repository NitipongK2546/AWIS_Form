from django import forms
import warrant_form.forms_central as CentralForm

arrest_result_choices = (
    # (0, "ยังไม่ได้รายงานผล"),
    (1, "จับได้"),
    (2, "อื่น ๆ")
)

class ReportWarrantForm(forms.Form):
    # court_code = forms.CharField(required=False, ) 
    # woa_type = forms.CharField(required=False, )
    # woa_year = forms.CharField(required=False, )
    # woa_no = forms.CharField(required=False, )
    # req_num_case_type_id = forms.CharField(required=False, )
    # arrest_report_date = forms.CharField(required=False, )
    # arrest_report_uid = forms.CharField(required=False, )

    arrest_result = forms.CharField(required=False, widget=forms.Select(choices=arrest_result_choices))

    arrest_date_day = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.day_choices))
    arrest_date_month = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.month_choices, attrs={
        'onchange': 'changeDate(arrest_date_day, arrest_date_month, arrest_date_year)'
    }))
    arrest_date_year = forms.IntegerField(required=False, widget=forms.Select(choices=CentralForm.year_choices, attrs={
        'onchange': 'changeDate(arrest_date_day, arrest_date_month, arrest_date_year)'
    }))

    arrest_result_other_text = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 80,
                "style": "resize: vertical; width:95%;",
                "placeholder": "รายละเอียดเพิ่มเติม...",
            }
        )
    )
    
    arrest_officer_name = forms.CharField(required=False, max_length=250)