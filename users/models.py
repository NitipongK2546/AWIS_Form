from django.db import models
from django.contrib.auth.models import AbstractUser
from awis_custom_settings import settings
from .permissions import permissions as perms
from users.permissions import PermissionList, PermissionType
from awis_custom_settings.settings import RoleChoices, RoleList
from django.contrib.auth import get_user_model

from django.utils import timezone

LOG_DIR = "output/"

# Create your models here.

DEFAULT_ROLE = RoleList.getDefaultRoleChoiceAssigned()

class UserDataModel(AbstractUser):
    api_uid = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def getUserLog(self):
        all_logs = LogSystem.objects.filter(user_id=self.api_uid)

        return all_logs
        
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

class LogSystem(models.Model):
    user_id : int = models.IntegerField()
    action : PermissionType = models.CharField()
    system : PermissionList = models.CharField()
    time_logged : timezone.datetime = models.DateTimeField()

    def __str__(self):
        user_obj = UserDataModel.objects.get(api_uid=self.user_id)
        return f"[{self.time_logged.astimezone(timezone.get_current_timezone())}]: {user_obj.username} ({user_obj.first_name} {user_obj.last_name}) {self.action.value.capitalize()} the {self.system.value.capitalize()}"
    
    def createLog(self, filename):
        createLog(self.user_id, self.action, self.system, filename)

def createLog(user_id : int, action : PermissionType, system : PermissionList, filename : str = "access_log.txt") -> LogSystem:

    time_logged : timezone.datetime = timezone.now()

    log_obj = LogSystem.objects.create(user_id=user_id, action=action, system=system, time_logged=time_logged)

    with open(LOG_DIR + filename, mode="a", encoding="utf-8") as file:
        file.write(f"{log_obj}\n")

    return log_obj  

def exportLogAsFile(filename : str = "all_access_log.txt"):
    all_logs = LogSystem.objects.all()

    with open(LOG_DIR + filename, mode="a", encoding="utf-8") as file:
        for log in all_logs:
            file.write(f"{log}\n")
    

def getUserLog(user_id : int):
    all_logs = LogSystem.objects.filter(user_id=user_id)

    return all_logs

###############################################################################
