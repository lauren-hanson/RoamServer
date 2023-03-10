from django.db import models

class TripTag(models.Model):
    
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name='trip_tags')
    tag = models.ForeignKey("Tag", on_delete=models.SET_NULL, related_name='tag_trips', null=True)