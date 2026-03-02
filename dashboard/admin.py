from django.contrib import admin
from dashboard.models import FormApprovalDataContainer

# Register your models here.

@admin.register(FormApprovalDataContainer)
class UserDataModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'approve_status', 'form_creator', 'date_created')