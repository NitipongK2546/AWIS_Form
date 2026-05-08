from django.db import models

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