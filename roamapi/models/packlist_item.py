from django.db import models

class PackListItem(models.Model):
    name = models.CharField(max_length = 50)