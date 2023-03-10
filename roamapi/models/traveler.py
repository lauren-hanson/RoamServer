from django.db import models
from django.contrib.auth.models import User


class Traveler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=250)
    followers = models.ManyToManyField("Traveler", through="Follower", related_name="follower")


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def follow(self):
        return self.__follow

    @follow.setter
    def follow(self, value):
        self.__follow = value