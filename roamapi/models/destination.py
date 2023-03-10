from django.db import models

class Destination(models.Model):
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    latitude = models.FloatField(max_length=25)
    longitude = models.FloatField(max_length=25)
    