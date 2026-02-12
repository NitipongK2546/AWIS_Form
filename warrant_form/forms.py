from django.forms import ModelForm
from warrant_form.models import ArrayWarrantDataModel, MainJSONWarrantDataModel

class MainJSONWarrantForm(ModelForm):
    class Meta:
        model = MainJSONWarrantDataModel
        exclude = ["warrants",]

class ArrayWarrantForm(ModelForm):
    class Meta:
        model = ArrayWarrantDataModel
        fields = "__all__"