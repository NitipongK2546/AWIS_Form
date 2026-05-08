from django.db import models

class SelectedCourt(models.Model):
    data : dict = models.JSONField(default=dict)