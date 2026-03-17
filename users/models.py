from django.db import models
from django.contrib.auth.models import User
from admin_panel.forms import CustomizedUserCreationForm


# Create your models here.

class UserDataModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    role = models.IntegerField(choices=CustomizedUserCreationForm.RoleChoices)

    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # May be unused. Here for now.
    api_uid = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class OTPCollection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return f"OTP secret for {self.user.username}"
