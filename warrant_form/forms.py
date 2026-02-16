from django import forms
from warrant_form.models import WarrantDataModel, MainAWISDataModel

class MainAWISForm(forms.ModelForm):
    class Meta:
        model = MainAWISDataModel
        exclude = ["scene_date","warrants"]
        # fields = "__all__"
        widgets = {
            'scene_date_datehalf': forms.DateInput(attrs={'type': 'date'}),
            'scene_date_timehalf': forms.TimeInput(attrs={'type': 'time'}),
        }

class WarrantForm(forms.ModelForm):
    class Meta:
        model = WarrantDataModel
        fields = "__all__"