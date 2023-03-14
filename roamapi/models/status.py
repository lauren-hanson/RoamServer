from django.db import models 

class Status(models.Model): 

    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    quickStop = models.BooleanField(default=False)
    finalDestination = models.BooleanField(default=False)
    