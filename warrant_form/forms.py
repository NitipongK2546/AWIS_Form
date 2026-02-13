from django import forms
from warrant_form.models import WarrantDataModel, MainAWISDataModel

class MainAWISForm(forms.ModelForm):
    class Meta:
        model = MainAWISDataModel
        # exclude = ["warrants",]
        fields = "__all__"
        widgets = {
            'scene_date': forms.SplitDateTimeWidget(
                date_attrs={
                    "type": "date", 
                    "class": "form-control",
                    # "placeholder": "วัน-เดือน-ปี"
                },
                time_attrs={
                    "type": "time", 
                    "class": "form-control",
                    # "placeholder": ""
                },
            ),
        }

class WarrantForm(forms.ModelForm):
    class Meta:
        model = WarrantDataModel
        fields = "__all__"