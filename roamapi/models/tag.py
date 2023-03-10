from django.db import models

class Tag(models.Model):
    type = models.CharField(max_length = 50)