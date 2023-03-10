from django.db import models

class PackListCategory(models.Model):
    label = models.CharField(max_length = 50)