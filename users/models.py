from django.db import models
from django.contrib.auth.models import AbstractUser
from awis_custom_settings import settings
from .permissions import permissions as perms
from users.permissions import PermissionList, PermissionType
from awis_custom_settings.settings import RoleChoices, RoleList
from django.contrib.auth import get_user_model

from django.utils import timezone
import os


# Create your models here.

DEFAULT_ROLE = RoleList.getDefaultRoleChoiceAssigned()

class UserDataModel(AbstractUser):
    api_uid = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def getUserLog(self):
        all_logs = LogSystem.objects.filter(user_id=self.api_uid)

        return all_logs
    
    def getGroupString(self):
        group_list = list(self.groups.all())
        return [group.name for group in group_list]
        
class UserAccess(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=250)
    department = models.CharField(max_length=200)
    role = models.IntegerField(
        choices=RoleChoices.choices,
        default=DEFAULT_ROLE
    )

def create_superuser():
    User : UserDataModel = get_user_model()

    user = User.objects.filter(
        username="admin",
    ).first()

    if user:
        return

    user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass999999",
    )

    user.first_name = "Mr. Admin"
    user.last_name = "Superuser"

    user.api_uid = 9_999_999

    user.save()

############################################################################

class OTPCollection(models.Model):
    user = models.OneToOneField(UserDataModel, on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return f"OTP secret for {self.user.username}"
    
###############################################################################

log_type = (
    ("normal", "normal"),
    ("errors", "errors"),
    ("denied", "denied"),
)

class LogSystem(models.Model):
    user_id : int = models.IntegerField()
    action : str = models.CharField()
    system : str = models.CharField()
    time_logged : timezone.datetime = models.DateTimeField()
    relevant_info : list = models.JSONField(blank=True, null=True,)
    type : int = models.CharField(max_length=6, choices=log_type)

    def __str__(self):
        datetime_info = self.time_logged.astimezone(timezone.get_current_timezone())

        user_obj = UserDataModel.objects.get(api_uid=self.user_id)
        user_info = f"{user_obj.getGroupString()} {user_obj.username} ({user_obj.first_name} {user_obj.last_name})"

        action_info = f"{self.action} -> {self.system}"

        ####

        basic_info : str = f"[{datetime_info}]: {user_info} {action_info}"

        return basic_info
    
    def toStrFailed(self, reason : str, url_path : str = ""):
        current_string = f"{self}"
        if url_path:
            current_string = f"{current_string} (Path: {url_path})"

        if not self.relevant_info:
            return current_string
        
        info_list : list[str] = self.relevant_info

        affected_obj = ""

        for info in info_list:
            affected_obj = affected_obj + f"{info}, "

        failed_info : str = f"{reason}: [ {affected_obj} ]"

        return f"{self} | {failed_info}"
        # return f"{failed_info} | {self}"

    def toStrExtra(self, url_path : str = ""):
        current_string = f"{self}"
        if url_path:
            current_string = f"{current_string} (Path: {url_path})"

        if not self.relevant_info:
            return current_string
        
        info_list : list[str] = self.relevant_info

        affected_obj = ""

        for info in info_list:
            affected_obj = affected_obj + f"{info}, "

        extra_info : str = f"Affected: [ {affected_obj} ]"

        return f"{current_string} | {extra_info}"

    # def createLog(self, filename):
    #     createLog(self.user_id, self.action, self.system, filename)

###############################################################################

# class PathPermission(models.Model):
#     url_path : dict = models.JSONField(default=dict)

#     def get_perms(self, view_name : str) -> list[str] | None:
#         return self.url_path.get(view_name)

#     def set_perms(self, view_name : str, perms : list[str]):
#         self.url_path.update({view_name: perms})
#         self.save()

#     @staticmethod
#     def add_perms(view_name : str, perm_list : list[str]):
#         target_obj = PathPermission.objects.all().first()
#         target_list : list[str] = target_obj.url_path.get(view_name)
#         # if not target_list:
#         #     target_obj.url_path.update({view_name: []})

#         for perm in perm_list:
#             if perm not in target_list:
#                 target_list.append(perm)

#         target_obj.save()

#     @staticmethod
#     def delete_perms(view_name : str, perm : str):
#         target_obj = PathPermission.objects.first()
#         target_list : list = target_obj.url_path.get(view_name)
#         target_list.remove(perm)
#         target_obj.save()

#     @staticmethod
#     def of_view(target_view : str) -> list[str]:
#         path_perm = PathPermission.objects.first()

#         required_permissions = path_perm.get_perms(target_view)
#         if not required_permissions:
#             return []

#         return required_permissions
    
#     @staticmethod
#     def get_all_perms() -> dict:
#         path_perm = PathPermission.objects.all().first()
#         return path_perm.url_path
    
#     def get_all_keys() -> list[str]:
#         path_perm = PathPermission.objects.all().first()
#         output_list = [(key, key) for key in path_perm.url_path.keys()]

#         return output_list

# PathPermission.objects.create(url_path=)

# {
    
# }