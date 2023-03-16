from django.db import models

class State(models.Model):
    label = models.CharField(max_length = 50)