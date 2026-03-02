from django.contrib import admin
from users.models import UserDataModel 

# Register your models here.

@admin.register(UserDataModel)
class UserDataModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
