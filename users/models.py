from django.db import models
from django.contrib.auth.models import AbstractUser
from awis_custom_settings import settings
from .permissions import permissions as perms
from awis_custom_settings.settings import RoleChoices, RoleList
from django.contrib.auth import get_user_model

# Create your models here.

DEFAULT_ROLE = RoleList.getDefaultRole()

class UserDataModel(AbstractUser):
    # role = models.IntegerField(choices=settings.RoleChoices, default=DEFAULT_ROLE)

    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # May be unused. Here for now.
    api_uid = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
class UserAccess(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=250)
    department = models.CharField(max_length=200)
    role = models.IntegerField(
        choices=RoleChoices.choices,
        default=DEFAULT_ROLE
    )

class OTPCollection(models.Model):
    user = models.OneToOneField(UserDataModel, on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return f"OTP secret for {self.user.username}"

def create_superuser():
    User = get_user_model()

    user = User.objects.filter(
        username="admin",
    ).first()

    if user:
        return

    user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass999999",
        role=99,
    )

    user.first_name = "Mr. Admin"
    user.last_name = "Superuser"

    user.save()

# def create_user():
#     User = get_user_model()

#     user = User.objects.filter(
#         username=self.username,
#     ).first()

#     if user:
#         return

#     user = User.objects.create_user(
#         username="admin",
#         email="admin@example.com",
#         password="adminpass999999"
#     )

#     user.first_name = "Mr. Admin"
#     user.last_name = "Superuser"
#     user.save()