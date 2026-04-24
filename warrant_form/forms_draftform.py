from django import forms
from .model_draftform import ReqformDraftDataModel

class ReqformDraftModelForm(forms.ModelForm):
    class Meta:
        model = ReqformDraftDataModel
        fields = "__all__"