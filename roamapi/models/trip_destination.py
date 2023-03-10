from django.db import models


class TripDestination(models.Model):
    trip = models.ForeignKey(
        "Trip", on_delete=models.CASCADE, related_name='trip_destination')
    destination = models.ForeignKey(
        "Destination", on_delete=models.CASCADE, related_name='destination_trip')
    status = models.ForeignKey(
        "Status", on_delete=models.CASCADE, related_name='destination_status', null=True)
