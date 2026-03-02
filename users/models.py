from django.db import models
from django.contrib.auth.models import User, Group, Permission

import uuid

# Create your models here.

class UserDataModel(models.Model):

    class RoleChoices(models.IntegerChoices):
        EMPLOYEE = (0, "Employee") 
        MANAGER = (1, "Manager")
        DIRECTOR = (2, "Director")
        SYSTEM_ADMIN = (99, "System Admin")


    user = models.OneToOneField(User, on_delete=models.PROTECT)
    role = models.IntegerField(choices=RoleChoices)

    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # May be unused. Here for now.
    api_uid = models.IntegerField(blank=True, null=True)

    


