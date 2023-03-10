from django.db import models

class Weather(models.Model):
    destination = models.ForeignKey("Destination", on_delete=models.CASCADE, related_name='destination_tags')