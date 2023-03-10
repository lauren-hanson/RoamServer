from django.db import models

class Comment(models.Model):

    traveler = models.ForeignKey("Traveler", null=True, blank=True, on_delete=models.CASCADE, related_name='traveler_comment')
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name='trip_comment')
    content = models.CharField(max_length=300)

    @property
    def writer(self):
        return self.__writer

    @writer.setter
    def writer(self, value):
        self.__writer = value