from django.db import models

import hashlib
import secrets
import os

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
    hashed_api_key = models.CharField(max_length=64)
    salt = models.CharField(max_length=16)
    permissions : list[dict] = models.JSONField(default=list)
    owner = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}: {self.permissions}"

    @staticmethod
    def createAPIKey(request : HttpRequest, permissions : list[dict]):
        salt = secrets.token_hex(8)
        api_key = api_key = secrets.token_hex(32)

        hashed_key = hashlib.sha256((salt + api_key).encode())

        result = APISecret.objects.filter(owner=request.user)
        if result:
            result.update(
                hashed_api_key = hashed_key.hexdigest(),
                salt = salt,
                permissions = permissions,
            )
        else:
            APISecret.objects.create(
                hashed_api_key = hashed_key.hexdigest(),
                salt = salt,
                permissions = permissions,
                owner = request.user,
            )

        return api_key
    
    @staticmethod
    def checkAPIKey(api_key : str):
        result = False

        for api_obj in APISecret.objects.all():
            salt = api_obj.salt
            hash = hashlib.sha256((salt + api_key).encode())

            if hash.hexdigest() == api_obj.hashed_api_key:
                result = True
                break
        
        return result