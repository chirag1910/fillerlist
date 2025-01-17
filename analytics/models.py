from django.db import models
from analytics.manager import AnalyticManager

class Analytic(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip_address = models.fields.GenericIPAddressField(blank=True, null=True)
    time = models.fields.DateTimeField()

    objects = AnalyticManager()

    class Meta:
        ordering = ["time"]
