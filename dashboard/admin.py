from django.contrib import admin
from dashboard.models import VisualFormApprovalData

# Register your models here.

@admin.register(VisualFormApprovalData)
class UserDataModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'approve_status', 'form_creator', 'date_created')