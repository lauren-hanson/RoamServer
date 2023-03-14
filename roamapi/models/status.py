from django.db import models 

class Status(models.Model): 

    isHome = models.BooleanField(default=False)
    isFinalDestination = models.BooleanField(default=False)
    isStop = models.BooleanField(default=False)
    