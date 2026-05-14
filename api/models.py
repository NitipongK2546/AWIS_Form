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

class APISecret(models.Model):
    hashed_api_key = models.CharField(max_length=64)
    salt = models.CharField(max_length=16)
    permissions : list[dict] = models.JSONField(default=list)

    @staticmethod
    def createAPIKey(permissions : list[dict]):
        salt = secrets.token_hex(8)
        api_key = api_key = secrets.token_hex(32)

        hashed_key = hashlib.sha256(salt + api_key)
        
        APISecret.objects.create(
            hashed_api_key = hashed_key,
            salt = salt,
            permissions = permissions,
        )

        return api_key
    
    def checkAPIKey(self, api_key : str):
        salt = self.salt
        result = hashlib.sha256(salt + api_key)

        if result == self.hashed_api_key:
            return True
        
        return False