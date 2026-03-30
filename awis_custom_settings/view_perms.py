from django.db import models
from enum import Enum

from users.permissions import perm_str_list, perm_str
from users.permissions import PermissionList as N, PermissionType as T

class PermissionRequiredForView(Enum):
    CREATE_REQFORM = perm_str(T.CREATE, N.REQFORM_AWAIT_APPROVAL)
    

# class PermissionRequiredForView(models.Model):
