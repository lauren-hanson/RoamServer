from django.db import models

class Subscription(models.Model):
    traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE, related_name='traveler_with_subscribers')
    subscriber = models.ForeignKey('Traveler', on_delete=models.CASCADE, related_name='subscribed_follower')
    created_on = models.DateField(auto_now=False, auto_now_add=True)
