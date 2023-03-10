from django.db import models

class TripPackList(models.Model):

    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name='trip_list')
    packlist = models.ForeignKey("PackList", on_delete=models.SET_NULL, related_name='pack_list', null=True)