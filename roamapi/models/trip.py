from django.db import models


class Trip(models.Model):
    traveler = models.ForeignKey("Traveler", on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    end_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    notes = models.CharField(max_length=500)
    public = models.BooleanField(default=False)
    destinations = models.ManyToManyField("Destination", through="TripDestination", related_name='destinations_of_trip')
    weather = models.CharField(max_length=300),
    tags = models.ManyToManyField("Tag", through="TripTag", related_name='tags_of_post')

    @property
    def writer(self):
        return self.__writer

    @writer.setter
    def writer(self, value):
        self.__writer = value