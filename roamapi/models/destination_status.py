from django.db import models

class DestinationStatus(models.Model):

    type = models.CharField(max_length=50, null=True)
