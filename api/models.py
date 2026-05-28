from django.db import models

import hashlib
import secrets

class HealthCheckStatus(models.Model):
    status = models.BooleanField()
    last_date = models.DateTimeField(auto_now=True)

    @staticmethod
    def updateStatus(current_status : bool):
        if HealthCheckStatus.objects.count() < 3:
            HealthCheckStatus.objects.create(
                status=current_status
            )
        else:
            HealthCheckStatus.objects.first(
                status=current_status
            ).delete()
            HealthCheckStatus.objects.create(
                status=current_status
            )

    @staticmethod
    def isHealthOK():
        latest_check = HealthCheckStatus.objects.last()

        if latest_check.status:
            return True
        
        return False


class ExternalSelectorData(models.Model):
    name = models.CharField(max_length=64)
    hash_hex_str = models.CharField(max_length=40)
    data : dict = models.JSONField(default=dict)
    prev_data : dict = models.JSONField(default=dict)

    def isHashDifferent(self, new_hash_str : str) -> bool:
        if not new_hash_str:
            return False

        if self.hash_hex_str != new_hash_str:
            return True
        
        return False

    def replaceData(self, incoming_data : dict):
        self.hash_hex_str = incoming_data.get("hash_hex_str")
        self.prev_data = self.data
        self.data = incoming_data.get("data")
        self.save()

from users.models import UserAccess, UserDataModel
from django.http import HttpRequest

class APISecret(models.Model):
    owner = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    hashed_api_key = models.CharField(max_length=64)
    identifier = models.CharField(max_length=16, unique=True)
    salt = models.CharField(max_length=16)
    permissions : dict[str] = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.owner}: {self.permissions}"

    @staticmethod
    def createAPIKey(request : HttpRequest, permissions : dict[str]):
        salt = secrets.token_hex(8)
        api_key = api_key = secrets.token_hex(32)

        hashed_key = hashlib.sha256((salt + api_key).encode())

        identifier = _createIdentifier()

        result = APISecret.objects.filter(owner=request.user.pk)
        if result:
            result.update(
                hashed_api_key = hashed_key.hexdigest(),
                salt = salt,
                permissions = permissions,
                identifier = identifier,
            )
        else:
            APISecret.objects.create(
                hashed_api_key = hashed_key.hexdigest(),
                salt = salt,
                permissions = permissions,
                owner = request.user,
                identifier = identifier,
            )

        return (identifier + api_key)
    
    @staticmethod
    def checkAPIKey(api_key_with_id : str):
        result = False

        identifier = api_key_with_id[:16]
        key = api_key_with_id[16:]

        api_obj = APISecret.checkIdentifier(identifier)

        if api_obj:
            salt = api_obj.salt
            hash = hashlib.sha256((salt + key).encode())

            if hash.hexdigest() == api_obj.hashed_api_key:
                result = api_obj.permissions
        
        return result
    
    @staticmethod
    def checkIdentifier(identifier : str):
        api_obj = APISecret.objects.filter(identifier=identifier).first()

        if api_obj:
            return api_obj
        
        return None
    
def _createIdentifier():
    while True:
        identifier = secrets.token_hex(8)

        if not APISecret.checkIdentifier(identifier):
            return identifier