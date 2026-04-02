# from django import forms
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