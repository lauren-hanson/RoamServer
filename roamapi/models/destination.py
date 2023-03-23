from django.db import models

class Destination(models.Model):

    location = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    latitude = models.FloatField(max_length=25, null=True, blank=True)
    longitude = models.FloatField(max_length=25, null=True, blank=True)
    status = models.ForeignKey('status', on_delete=models.CASCADE, related_name='destination_status', null=True)