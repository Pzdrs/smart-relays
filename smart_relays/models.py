from django.db import models


class ApplicationData(models.Model):
    key = models.CharField(max_length=255, unique=True)
    data = models.JSONField(default=dict)
