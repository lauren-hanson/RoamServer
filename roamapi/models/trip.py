from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    traveler = models.ForeignKey("Traveler", on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True)
    image_url = models.CharField(max_length=250, blank=True)
    start_date = models.DateField(
        null=True, blank=True, auto_now=False, auto_now_add=False)
    end_date = models.DateField(
        null=True, blank=True, auto_now=False, auto_now_add=False)
    weather = models.CharField(max_length=300, blank=True)
    notes = models.CharField(max_length=500)
    public = models.BooleanField(default=False)
    destination = models.ManyToManyField(
        "Destination", through="TripDestination")
    tag = models.ManyToManyField(
        "Tag", through="TripTag")

    @property
    def writer(self):
        return self.__writer

    @writer.setter
    def writer(self, value):
        self.__writer = value
