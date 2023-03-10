from django.db import models

class Follower(models.Model):

    traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE, related_name='traveler_follower')
    follower = models.ForeignKey('Traveler', on_delete=models.CASCADE, related_name='followed_traveler')